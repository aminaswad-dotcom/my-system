from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from models import db, User, Document, File
from sqlalchemy.orm import joinedload
from flask_login import current_user
from config import Config
import os
from datetime import datetime, date

import zipfile
import shutil
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import logging

app = Flask(__name__)
app.config.from_object(Config)

# Logging setup
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    submit = SubmitField('دخول')

class DocumentForm(FlaskForm):
    doc_number = StringField('رقم الكتاب', validators=[DataRequired()])
    date = DateField('التاريخ', validators=[DataRequired()], default=date.today)
    sender_receiver = StringField('الجهة', validators=[DataRequired(), Length(max=200)])
    subject = StringField('الموضوع', validators=[DataRequired(), Length(max=500)])
    notes = TextAreaField('ملاحظات')
    doc_type = SelectField('النوع', choices=[('وارد', 'وارد'), ('صادر', 'صادر')], validators=[DataRequired()])
    files = FileField('الملفات')
    submit = SubmitField('حفظ')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'jpg', 'jpeg', 'png', 'gif'}



# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('اسم المستخدم أو كلمة المرور خطأ')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    search = request.args.get('search', '')
    doc_type = request.args.get('type', '')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Document.query
    if search:
        query = query.filter(
            Document.doc_number.contains(search) |
            Document.sender_receiver.contains(search) |
            Document.subject.contains(search)
        )
    if doc_type:
        query = query.filter(Document.doc_type == doc_type)
    if start_date:
        query = query.filter(Document.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Document.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    documents = query.order_by(Document.date.desc()).all()
    return render_template('dashboard.html', documents=documents, search=search, doc_type=doc_type, start_date=start_date, end_date=end_date)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_document():
    form = DocumentForm()
    if form.validate_on_submit():
        doc = Document(
            doc_number=form.doc_number.data,
            date=form.date.data,
            sender_receiver=form.sender_receiver.data,
            subject=form.subject.data,
            notes=form.notes.data,
            doc_type=form.doc_type.data
        )
        db.session.add(doc)
        try:
            db.session.commit()
            app.logger.info(f"Document {doc.id} created successfully")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Failed to save document {doc.doc_number}: {str(e)}")
            flash('خطأ في حفظ الوثيقة، حاول مرة أخرى')
            return render_template('add_document.html', form=form)
        
        # Handle files
        if 'files' in request.files:
            files = request.files.getlist('files')
            doc_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(doc.id))
            os.makedirs(doc_dir, exist_ok=True)
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(doc_dir, filename)
                    file.save(filepath)
                    file_db = File(document_id=doc.id, filename=filename, filepath=filepath)
                    db.session.add(file_db)
        db.session.commit()
        flash('تم إضافة الوثيقة بنجاح')
        return redirect(url_for('dashboard'))
    return render_template('add_document.html', form=form)

@app.route('/public/document/<doc_id>')
def public_document(doc_id):
    doc = Document.query.options(joinedload(Document.files)).get_or_404(doc_id)
    return render_template('document.html', doc=doc, is_public=True)

@app.route('/document/<doc_id>')
@login_required
def document(doc_id):
    doc = Document.query.options(joinedload(Document.files)).get_or_404(doc_id)
    return render_template('document.html', doc=doc, is_public=False)



@app.route('/edit/<doc_id>', methods=['GET', 'POST'])
@login_required
def edit_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    form = DocumentForm(obj=doc)
    if form.validate_on_submit():
        doc.doc_number = form.doc_number.data
        doc.date = form.date.data
        doc.sender_receiver = form.sender_receiver.data
        doc.subject = form.subject.data
        doc.notes = form.notes.data
        doc.doc_type = form.doc_type.data
        try:
            db.session.commit()
            app.logger.info(f"Document {doc.id} updated successfully")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Failed to update document {doc.id}: {str(e)}")
            flash('خطأ في تعديل الوثيقة')
            return render_template('edit_document.html', form=form, doc=doc)
        flash('تم تعديل الوثيقة بنجاح')
        return redirect(url_for('dashboard'))
    return render_template('edit_document.html', form=form, doc=doc)

@app.route('/delete/<doc_id>')
@login_required
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    try:
        db.session.delete(doc)
        db.session.commit()
        app.logger.info(f"Document {doc_id} deleted")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Failed to delete document {doc_id}: {str(e)}")
        flash('خطأ في الحذف')
        return redirect(url_for('dashboard'))
    flash('تم حذف الوثيقة')
    return redirect(url_for('dashboard'))

@app.route('/upload/<doc_id>', methods=['GET', 'POST'])
@login_required
def upload_files(doc_id):
    doc = Document.query.get_or_404(doc_id)
    if request.method == 'POST':
        if 'files' in request.files:
            files = request.files.getlist('files')
            doc_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(doc.id))
            os.makedirs(doc_dir, exist_ok=True)
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(doc_dir, filename)
                    file.save(filepath)
                    file_db = File(document_id=doc.id, filename=filename, filepath=filepath)
                    db.session.add(file_db)
            try:
                db.session.commit()
                app.logger.info(f"Files uploaded to document {doc.id}")
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Failed to save files for document {doc.id}: {str(e)}")
                flash('خطأ في رفع الملفات')
                return render_template('upload_files.html', doc=doc)
            flash('تم رفع الملفات بنجاح')
            return redirect(url_for('document', doc_id=doc_id))
    return render_template('upload_files.html', doc=doc)

@app.route('/download/<file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(os.path.dirname(file.filepath), os.path.basename(file.filepath))

@app.route('/reports')
@login_required
def reports():
    report_type = request.args.get('type', 'daily')
    today = date.today()
    if report_type == 'monthly':
        start = today.replace(day=1)
        end = today
    else:
        start = end = today
    docs = Document.query.filter(Document.date >= start, Document.date <= end).all()
    return render_template('reports.html', docs=docs, report_type=report_type, start=start, end=end)

@app.route('/backup')
@login_required
def backup():
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}.zip'
        backup_path = os.path.join(app.config['BACKUP_FOLDER'], backup_name)
        
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add database (correct path)
            db_path = 'instance/database.db'
            if os.path.exists(db_path):
                zipf.write(db_path, 'database.db')
            else:
                raise FileNotFoundError(f"Database not found: {db_path}")
            
            # Add uploads (fixed arcname)
            upload_folder = app.config['UPLOAD_FOLDER']
            if os.path.exists(upload_folder):
                for root, dirs, files in os.walk(upload_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
        
        flash(f'تم إنشاء نسخة احتياطية: {backup_name}', 'success')
    except Exception as e:
        flash(f'خطأ في النسخ الاحتياطي: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# Create tables once on app startup (safe for prod)
with app.app_context():
    db.create_all()
    
    # Create default admin user if not exists (for production empty DB)
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        app.logger.info("Created default admin user: admin/admin123")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
