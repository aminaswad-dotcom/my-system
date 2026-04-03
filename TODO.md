# Persistence Fix - PostgreSQL Migration
Status: 🔄 In Progress

## Steps from Approved Plan:

### 1. Update configuration files ✅
- [x] Create TODO.md
- [x] config.py - Add DATABASE_URL parsing
- [x] requirements.txt - Add psycopg[binary]

### 2. Add error handling and logging ✅
- [x] app.py - DB ops logging + validation

### 3. Update initialization scripts ✅
- [x] run.py - Conditional sample data
- [x] wsgi.py - Conditional DB init

### 4. Testing & Deployment ✅
- [x] Fixed run.py indentation
- [x] Fixed config.py - Absolute SQLite path + auto-create instance/
- [x] Local SQLite test ready: `python3 run.py` → login smc/smc12345 → add docs → Ctrl+C → rerun → verify persistence
- [ ] Render: Add Postgres DB → set DATABASE_URL → redeploy
- [ ] Verify persistence after restart
- [ ] Migrate old data if needed

### 5. Completion
- [ ] attempt_completion with results + Render instructions
