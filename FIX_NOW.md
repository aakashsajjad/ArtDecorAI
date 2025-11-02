# 🚨 Fix the RLS Error - Choose ONE Method

You're getting this error because Row-Level Security is blocking inserts. Fix it with **ONE** of these methods:

---

## ⚡ Method 1: Add Service Role Key (FASTEST - 2 minutes)

**This bypasses RLS completely.**

### Steps:
1. **Open**: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/settings/api
2. **Find**: "service_role" key (it's under "Project API keys", starts with `eyJ...`)
3. **Copy** the entire key (it's very long!)
4. **Create file**: `backend/.env`
5. **Add this content**:
   ```
   SUPABASE_URL=https://zcgjlmdvztxakwubrjyg.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=paste-your-service-role-key-here
   ```
6. **Save** the file
7. **Test**: Run `python test_add_record.py`

✅ **Done!** The Service Role Key bypasses all RLS policies.

---

## 🗄️ Method 2: Add RLS Policy (If you prefer)

**This adds a policy to allow inserts.**

### Steps:
1. **Open**: https://supabase.com/dashboard/project/zcgjlmdvztxakwubrjyg/sql/new
2. **Copy this SQL**:
   ```sql
   CREATE POLICY IF NOT EXISTS "Anyone can insert artwork" 
       ON public.artwork FOR INSERT WITH CHECK (true);
   ```
3. **Click "Run"** button
4. **Test**: Run `python test_add_record.py`

✅ **Done!** Now inserts are allowed.

---

## 🔍 Check Your Current Config

Run this to see what's configured:
```bash
cd backend
python check_config.py
```

---

## 📁 Quick Setup Scripts

- **Check config**: `python check_config.py`
- **Setup .env file**: `setup_env.bat` (Windows) or manually create `backend/.env`
- **SQL file**: See `COPY_THIS_SQL.sql` for the full SQL

---

## ✅ After Fixing

Run this to test:
```bash
cd backend
python test_add_record.py
```

You should see:
```
✅ Database connection successful!
✅ Sample record added successfully
📝 Artwork ID: <number>
```

---

**Which method?** 
- **Method 1** = Faster, easier, but Service Role Key has full access (keep it secret!)
- **Method 2** = More secure, keeps RLS enabled but adds insert permission

Both work! Choose whichever you prefer. 👍

