from app import app, db
from models import User, Document, File
from config import Config
from datetime import date, datetime
import os

with app.app_context():
    db.create_all()
    
    # Create sample users if not exist
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin')
        db.session.add(admin)
    
    if not User.query.filter_by(username='user').first():
        user = User(username='user')
        user.set_password('user')
        db.session.add(user)
    
    # Sample documents
    if not Document.query.first():
        from datetime import date, timedelta
        dates = [date.today() - timedelta(days=i) for i in range(5)]
        doc_types = ['وارد', 'صادر']
        for i, d in enumerate(dates):
            doc = Document(
                doc_number=f'DOC-{i+1:03d}',
                date=d,
                sender_receiver='جهة حكومية',
                subject='موضوع الوثيقة',
                notes='ملاحظات',
                doc_type=doc_types[i%2]
            )
            db.session.add(doc)
        db.session.commit()
    
    Config.init_folders()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
