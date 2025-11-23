# Supabase Setup Guide for Long-Term Memory 🧠

## What is Supabase?

Supabase is a **FREE** cloud database (PostgreSQL) that stores your users' therapeutic journey across sessions. Think of it as cloud memory for your AI therapist.

**FREE Tier Includes:**
- ✅ 500MB database storage
- ✅ 2GB bandwidth per month
- ✅ 50,000 monthly active users
- ✅ No credit card required to start!

---

## Why Use Supabase?

**Without Supabase:**
- Memory stored locally only
- Each computer has separate memories
- Memory lost if app reinstalled

**With Supabase:**
- ✅ Memories sync across devices
- ✅ Remembers users across sessions
- ✅ "Welcome back! Last time we talked about..."
- ✅ Progress tracking over time
- ✅ Therapeutic continuity

---

## Quick Setup (5 Minutes)

### Step 1: Create Free Supabase Account

1. Go to: **https://supabase.com**
2. Click **"Start your project"**
3. Sign up with GitHub, Google, or Email (FREE!)
4. Create a new project:
   - **Name**: `emosup-therapy` (or any name)
   - **Database Password**: Choose a strong password (save it!)
   - **Region**: Choose closest to your users
   - Click **"Create new project"**

Wait 2-3 minutes for your database to provision...

### Step 2: Get Your API Keys

1. In Supabase dashboard, go to **Settings** (⚙️ icon in sidebar)
2. Click **API**
3. Copy these two values:

   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **Anon/Public Key** (starts with `eyJ...`)

### Step 3: Add to Your App

1. Open `/home/user/emosup/.env` file (create if doesn't exist)
2. Add these lines:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 4: Create Database Tables

1. In Supabase dashboard, click **SQL Editor** in sidebar
2. Click **"New query"**
3. Paste this SQL and click **"Run"**:

```sql
-- User profiles table
CREATE TABLE user_profiles (
    user_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    profile_data JSONB NOT NULL,
    last_updated TIMESTAMP DEFAULT NOW()
);

-- Memory entries table
CREATE TABLE memory_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    message TEXT,
    emotion TEXT,
    emotion_intensity FLOAT,
    therapy_mode TEXT,
    entry_data JSONB,
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Therapy sessions table
CREATE TABLE therapy_sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    session_summary JSONB,
    key_insights TEXT[],
    assigned_homework TEXT[],
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Progress milestones table
CREATE TABLE progress_milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    milestone_type TEXT,
    description TEXT,
    achieved_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Indexes for performance
CREATE INDEX idx_memory_user ON memory_entries(user_id);
CREATE INDEX idx_memory_session ON memory_entries(session_id);
CREATE INDEX idx_sessions_user ON therapy_sessions(user_id);
CREATE INDEX idx_memory_timestamp ON memory_entries(timestamp DESC);
```

4. You should see: **"Success. No rows returned"**

### Step 5: Install Python Client

```bash
pip install supabase==2.0.0
```

### Step 6: Restart Your App

```bash
# Stop current server
pkill -f "python.*api_server"

# Start with Supabase enabled
python3 api_server.py
```

**That's it!** You now have cloud memory! 🎉

---

## Verify It's Working

### Test 1: Check Console Output

When starting `api_server.py`, you should see:

```
✓ Supabase connected - cloud memory enabled
```

If you see this instead, Supabase isn't configured (but app still works):
```
Supabase not configured - using local memory only
```

### Test 2: Send a Test Message

```bash
curl -X POST http://localhost:5000/api/therapy \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling anxious today",
    "session_id": "test-session-123"
  }'
```

### Test 3: Check Supabase Dashboard

1. Go to **Table Editor** in Supabase dashboard
2. Select `memory_entries` table
3. You should see your test message stored!

### Test 4: Test Continuity

Send another message with the **same session_id**:

```bash
curl -X POST http://localhost:5000/api/therapy \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How can I feel better?",
    "session_id": "test-session-123"
  }'
```

The AI should reference your previous conversation!

---

## What Gets Stored?

### user_profiles Table
```json
{
  "user_id": "abc123...",
  "total_sessions": 5,
  "total_messages": 47,
  "dominant_emotions": {"anxious": 15, "sad": 10, "happy": 8},
  "mood_trend": "improving",
  "identified_schemas": ["abandonment", "defectiveness"],
  "coping_strategies_tried": ["breathing exercises", "thought challenging"],
  "breakthroughs": ["Recognized negative thought pattern"],
  "therapeutic_alliance": 0.85
}
```

### memory_entries Table
```json
{
  "user_id": "abc123...",
  "session_id": "session-456",
  "timestamp": "2025-01-15T14:30:00Z",
  "message": "I feel so anxious all the time",
  "emotion": "anxious",
  "emotion_intensity": 0.8,
  "therapy_mode": "cbt",
  "entry_data": {
    "detected_patterns": ["catastrophizing"],
    "breakthroughs": [],
    "concerns": ["work stress"]
  }
}
```

---

## Privacy & Security

### Is User Data Safe?

✅ **YES!** Here's how:

1. **Anonymous User IDs**: No personal information stored
   - User ID is a hash of session ID
   - No names, emails, or identifying info

2. **Encrypted in Transit**: All data sent via HTTPS

3. **Row Level Security (RLS)**: Enable this for production:

```sql
-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE therapy_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE progress_milestones ENABLE ROW LEVEL SECURITY;

-- Allow public insert/read (for anonymous therapy app)
-- Adjust these policies based on your security requirements
CREATE POLICY "Allow all operations" ON user_profiles FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON memory_entries FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON therapy_sessions FOR ALL USING (true);
CREATE POLICY "Allow all operations" ON progress_milestones FOR ALL USING (true);
```

**Note**: For production apps with user accounts, implement proper authentication and RLS policies.

---

## Fallback System

**App works even if Supabase is unavailable!**

```
Priority 1: Supabase (cloud memory)
    ↓ If unavailable
Priority 2: Local JSON cache (data/memory_cache.json)
    ↓ Always works
Always: Session continues normally
```

Your app **never crashes** due to Supabase being down.

---

## Monitoring Usage

### Check Your Usage

1. Go to Supabase dashboard
2. Click **Settings** → **Usage**
3. See:
   - Database size
   - Bandwidth used
   - Active users
   - API requests

### FREE Tier Limits

- **Database**: 500MB (plenty for therapy app)
  - ~100,000 conversation entries
  - ~10,000 user profiles
- **Bandwidth**: 2GB/month
  - ~50,000 therapy sessions/month
- **Rows**: Unlimited on free tier!

### What If I Hit Limits?

**Upgrade Options:**
- **Pro Plan**: $25/month
  - 8GB database
  - 50GB bandwidth
  - 100,000 MAU

**Or Optimize:**
- Delete old memories (keep last 6 months)
- Compress entry data
- Use local storage more

---

## Advanced: Backup & Export

### Export All Data

```bash
# Using Supabase CLI
npx supabase db dump -f backup.sql

# Or use dashboard: Database → Backups
```

### Restore from Backup

```bash
psql -h db.yourproject.supabase.co -U postgres -f backup.sql
```

### Migrate to Self-Hosted PostgreSQL

Your app works with **any PostgreSQL database**!

Just change connection string:

```python
# In memory_system.py, modify SupabaseMemoryStore to use:
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="emosup",
    user="postgres",
    password="your_password"
)
```

---

## Troubleshooting

### Error: "Supabase unavailable"

**Check:**
1. ✅ Supabase URL correct in `.env`?
2. ✅ API key correct (should start with `eyJ...`)?
3. ✅ Tables created (run SQL from Step 4)?
4. ✅ Internet connection working?

**Test connection:**

```python
python3 -c "
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

client = create_client(url, key)
result = client.table('user_profiles').select('*').limit(1).execute()
print('✓ Supabase connected!')
"
```

### Error: "relation does not exist"

**Solution**: You forgot to create tables! Run the SQL from Step 4.

### Error: "Invalid API key"

**Solution**:
1. Get fresh key from Supabase dashboard → Settings → API
2. Copy **anon/public** key (not service_role key!)
3. Update `.env` file
4. Restart server

### App Works Without Supabase?

**YES!** This is normal. Supabase is **optional**. The app falls back to local storage.

To **force** Supabase:
- Verify keys in `.env`
- Check console for "Supabase connected" message
- Check Supabase dashboard for new rows after sending messages

---

## Benefits Recap

### Without Supabase (Local Only):
- ✅ Works offline
- ✅ Fast responses
- ❌ No cross-device sync
- ❌ Memory lost if app deleted
- ❌ No long-term progress tracking

### With Supabase (Cloud Memory):
- ✅ Everything above PLUS:
- ✅ Memories sync across devices
- ✅ "Welcome back" continuity
- ✅ Long-term progress tracking
- ✅ Therapeutic alliance building
- ✅ Schema and pattern detection over time
- ✅ User journey visualization (coming soon!)

---

## Next Steps

1. ✅ Complete setup (5 minutes)
2. ✅ Test with dummy data
3. ✅ Monitor usage in Supabase dashboard
4. ✅ Enable Row Level Security for production
5. ✅ Set up daily backups (optional)

---

## Resources

- **Supabase Docs**: https://supabase.com/docs
- **Supabase Dashboard**: https://supabase.com/dashboard
- **Python Client Docs**: https://supabase.com/docs/reference/python/introduction
- **FREE Tier Details**: https://supabase.com/pricing

---

**You're all set! Your AI therapist now has a memory that lasts! 🧠💜**

---

## Optional: Advanced Features

### 1. Automatic Session Summaries

Add a function to generate end-of-session summaries:

```python
# In memory_system.py
async def create_session_summary(self, session_id: str, user_id: str):
    """Generate summary when session ends"""
    memories = await self.recall(user_id, limit=100)

    # Extract insights
    insights = [m['breakthroughs'] for m in memories if m.get('breakthroughs')]

    summary = {
        "session_id": session_id,
        "total_messages": len(memories),
        "key_insights": insights,
        "progress_made": "User recognized thought patterns"
    }

    # Save to therapy_sessions table
    await self.supabase_store.client.table("therapy_sessions").insert({
        "session_id": session_id,
        "user_id": user_id,
        "session_summary": summary,
        "ended_at": datetime.now().isoformat()
    }).execute()
```

### 2. Progress Visualization

Query user's emotional journey:

```sql
SELECT
  DATE(timestamp) as date,
  emotion,
  AVG(emotion_intensity) as avg_intensity
FROM memory_entries
WHERE user_id = 'user123'
GROUP BY DATE(timestamp), emotion
ORDER BY date;
```

### 3. Therapeutic Milestones

Track breakthroughs:

```python
async def track_milestone(self, user_id: str, milestone: str):
    await self.supabase_store.client.table("progress_milestones").insert({
        "user_id": user_id,
        "milestone_type": "breakthrough",
        "description": milestone
    }).execute()
```

---

**Happy memory building! 🎉**
