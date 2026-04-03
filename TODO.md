# TODO: Fix PostgreSQL Table Creation on Render

**Plan Status:** Approved by user

**Completed Steps:**
- [x] Step 1: Edit app.py - Add db.create_all() in app context at module bottom
- [x] Step 2: Edit wsgi.py - Add db.init_app(application) before create_all
- [x] Step 3: Test changes locally with SQLite (server running successfully on port 5001, no errors)

**Completed Steps:**
- [x] Step 1: Edit app.py - Add db.create_all() in app context at module bottom
- [x] Step 2: Edit wsgi.py - Add db.init_app(application) before create_all
- [x] Step 3: Test changes locally with SQLite (server running successfully on port 5001, no errors)

**New Task - Create Initial Admin User:**
- [x] Step 7: Add admin user creation logic to app.py app_context block
- [x] Step 8: Test admin user locally (log shows "Created default admin user: admin/admin123")

**Remaining Steps:**
- [ ] Step 4: Commit and push to git for Render redeploy  
- [ ] Step 5: Verify production tables + admin user created (check Render logs)
- [ ] Step 6: Test login with admin/admin123 on Render
