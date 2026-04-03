import os
from app import app, db
from models import User, Document, File
from config import Config
from datetime import date, datetime
import os

with app.app_context():
    db.create_all()
    
    # Only create default user/sample data for local SQLite dev
    if 'sqlite' in Config.SQLALCHEMY_DATABASE_URI:
        # Create default user 'smc' if not exist
        if not User.query.filter_by(username='smc').first():
            smc_user = User(username='smc')
            smc_user.set_password('smc12345')
            db.session.add(smc_user)
            db.session.commit()
        
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
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False, use_debugger=True)
