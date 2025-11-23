# 🚀 ONE-COMMAND INSTALL - EmoSupport

## Windows - Super Simple!

### Step 1: Download
```
Click "Code" → "Download ZIP"
Extract to your computer
```

### Step 2: Run
```
Double-click: SETUP_AND_RUN.bat
```

**That's it!** The script will:
- ✅ Ask for your Groq API key (optional - press ENTER to skip)
- ✅ Install all dependencies
- ✅ Build the app
- ✅ Start the server
- ✅ Open your browser
- ✅ You're ready to use it!

---

## What Happens:

### First Time Running:
```
========================================
   EmoSupport - AI Therapy Companion
========================================

Optional: Groq API Key Setup
Enter your Groq API key (or press ENTER to skip):

[You paste your key or press ENTER]

Installing Dependencies...
✓ Python packages installed
✓ Node.js packages installed
✓ Frontend built

Starting EmoSupport Server...
✓ Server started!

Opening EmoSupport...

EmoSupport is running!
  Web Interface: http://localhost:3000/therapy
  API Server:    http://localhost:5000
```

### Next Time:
Just double-click `SETUP_AND_RUN.bat` again - it starts instantly!

---

## Optional: Get FREE Groq API Key (30 seconds)

**Want the BEST AI responses?**

1. Go to: **https://console.groq.com/keys**
2. Sign up (FREE, no credit card!)
3. Click "Create API Key"
4. Copy the key
5. Run `SETUP_AND_RUN.bat` again
6. Paste your key when asked
7. **Done!** Now you have enterprise-quality AI!

**Without Groq key:** App works with built-in responses (still great!)
**With Groq key:** Llama 3.3 70B AI (professional-grade therapy)

---

## Troubleshooting

### "Python not found"
1. Install Python 3.10+ from: https://www.python.org/downloads/
2. ✅ **Check** "Add Python to PATH" during installation
3. Restart your computer
4. Run `SETUP_AND_RUN.bat` again

### "Node.js not found"
**Option 1 (Recommended):**
1. Install Node.js from: https://nodejs.org/
2. Restart your computer
3. Run `SETUP_AND_RUN.bat` again

**Option 2 (Skip frontend):**
- API server still works!
- Use: http://localhost:5000/api/therapy
- Or build a custom frontend

### Server won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process
taskkill /PID [process_id] /F

# Try again
SETUP_AND_RUN.bat
```

### API key not working
1. Check your key at: https://console.groq.com/keys
2. Make sure you copied the **full key** (starts with `gsk_...`)
3. Edit `.env` file manually:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
4. Restart the server

---

## Advanced: Manual Setup

If you prefer manual control:

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Node.js dependencies
npm install

# 3. Build frontend
npm run build

# 4. Create .env file
echo GROQ_API_KEY=your_key_here > .env
echo NEXT_PUBLIC_API_BASE_URL=http://localhost:5000 >> .env

# 5. Start API server
python api_server.py

# 6. In another terminal, start frontend
npm run dev

# 7. Open browser
# http://localhost:3000/therapy
```

---

## Using Without Installation

### API Only (No UI):
```bash
# Start API server
python api_server.py

# Test it
curl -X POST http://localhost:5000/api/therapy \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel anxious", "session_id": "test"}'
```

### With Docker (Coming Soon):
```bash
docker run -p 5000:5000 emosup/therapy
```

---

## What You Get

### Without Groq API Key:
- ✅ Working AI therapist
- ✅ Emotion detection
- ✅ Therapeutic responses
- ✅ Voice interface
- ✅ Memory system
- ✅ Crisis detection
- ✅ **Works offline!**

### With Groq API Key (FREE):
- ✅ **Everything above PLUS:**
- ✅ Llama 3.3 70B AI
- ✅ Natural conversation
- ✅ Better responses
- ✅ Context awareness
- ✅ 30 requests/minute
- ✅ **Still FREE!**

---

## Features

- 💬 **Text Chat** - Type your feelings
- 🎤 **Voice Therapy** - Speak naturally
- 🎨 **Animated Blob** - Cute companion
- 🧠 **5 Therapy Frameworks** - ACT, CBT, DBT, Schema, Narrative
- 💾 **Long-Term Memory** - Remembers you across sessions
- 🔒 **100% Private** - All data stays on your computer
- 🆓 **Completely FREE** - No subscriptions ever

---

## System Requirements

- **OS:** Windows 7 or newer
- **RAM:** 2GB minimum (4GB recommended)
- **Disk:** 500MB free space
- **Python:** 3.10 or newer
- **Node.js:** 16 or newer (optional for frontend)
- **Internet:** Optional (for Groq API only)

---

## Privacy

- ✅ No account required
- ✅ No tracking
- ✅ No analytics
- ✅ Anonymous user IDs only
- ✅ Data stays on YOUR computer
- ✅ You own everything

---

## Support

**Need help?**
- 📖 Documentation: See `README.md`
- 🐛 Report issues: GitHub Issues
- 💬 Community: GitHub Discussions

**In crisis?**
- 🆘 Call 988 (US)
- 📱 Text HOME to 741741
- 🌍 International: https://www.iasp.info/resources/Crisis_Centres/

---

## One-Line Install (Alternative)

### Using Git:
```bash
git clone https://github.com/RHUDHRESH/emosup.git
cd emosup
SETUP_AND_RUN.bat
```

### Using curl (PowerShell):
```powershell
curl -L https://github.com/RHUDHRESH/emosup/archive/main.zip -o emosup.zip
Expand-Archive emosup.zip
cd emosup
SETUP_AND_RUN.bat
```

---

**Download now and start your healing journey! 💜**

🎉 **It literally takes 30 seconds to get started!** 🎉

---

*Questions? Check the full documentation in the repo.*
