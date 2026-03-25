# Remove QR Code from Document Detail Page - Implementation Plan

## Status: 📋 In Progress

### Step 1: [✅ DONE] Edit templates/document.html
- Remove col-md-4 QR sidebar completely
- Change col-md-8 to col-12 for full width details/files
- Keep all details, files, buttons unchanged

### Step 2: [✅ DONE] Edit app.py
- Remove qrcode/BytesIO imports
- Delete generate_qr() function entirely
- Remove generate_qr(doc_id) calls from document(), public_document(), upload_files routes
- Update render_template calls to remove qr_path parameter

### Step 3: [✅ DONE] Edit models.py
- Remove qr_code column from Document model

### Step 4: [⚠️ MANUAL] Database Migration
- No Flask-Migrate setup. To apply schema change:
  1. Stop app if running (Ctrl+C)
  2. `rm instance/database.db` to recreate clean DB (dev data loss)
  3. Restart app - new DB with updated schema (no qr_code column)
- Alternative: Use sqlite3 to DROP COLUMN manually if preserving data
- Run migration for models.py changes (if Flask-Migrate) or manual DB update
- Command: flask db migrate -m "remove qr_code"; flask db upgrade

### Step 5: [IN PROGRESS] Test Changes
- Restart app
- Test /document/<id>: details + files only, full width, no QR/errors
- Test public route and file upload
- Verify clean layout

### Step 6: [DONE] Cleanup (optional)
- Remove qrcode from requirements.txt
- Delete static/qr/ images if desired

**Next:** Starting Step 1
