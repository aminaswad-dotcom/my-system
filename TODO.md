# TODO: Fix QR Code Scanning to Open Corresponding File Directly

## Steps:
- [x] 1. Edit app.py: Import joinedload, modify generate_qr to use direct first file static URL if available
- [x] 2. Edit templates/document.html: Update QR section text to reflect direct file open
- [ ] 3. Delete existing static/qr/*.png to force regeneration
- [ ] 4. Restart server and test: Visit /document/<id> to regen QR, scan with phone app (should open file directly)
- [ ] 5. Mark complete
