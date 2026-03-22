# PythonAnywhere Deployment TODO

## [x] Step 1: Create WSGI file (wsgi.py)
- Create /home/systemproject1/systemproject1/wsgi.py with correct import.

## [ ] Step 2: Prepare project zip
- Run: `zip -r systemproject1.zip * -x "*.git*" "backups/*" "__pycache__/*" ".DS_Store" "TODO.md"`

## [ ] Step 3: Upload to PythonAnywhere
- Upload zip to /home/systemproject1/
- Unzip: `unzip systemproject1.zip`

## [ ] Step 4: Virtualenv setup
- Create venv: `/home/systemproject1/.virtualenvs/mysite`
- Activate & install: `pip install -r /home/systemproject1/systemproject1/requirements.txt`

## [ ] Step 5: Web app config
- Web tab: Add app → Python 3.10 → WSGI: `/home/systemproject1/systemproject1/wsgi.py`
- Static files: URL `/static/`, path `/home/systemproject1/systemproject1/static`
- Set env: `SECRET_KEY=your-super-secret-key-here`
- Reload app

## [ ] Step 6: Test
- Visit https://systemproject1.pythonanywhere.com/login (admin/admin)
- Add doc → Verify QR scans to live URL
- Upload files → Verify access/download

**Progress: Step 1 in progress**
