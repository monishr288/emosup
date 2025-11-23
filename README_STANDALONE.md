# EmoSupport - Standalone Desktop App 🚀

## Quick Start (No Installation Needed!)

### For Users

1. **Download** `EmoSupport.exe` from releases
2. **Double-click** to run
3. **Browser opens** automatically with your AI therapist
4. **Start talking!** - Text or voice, your choice

That's it! No installation, no setup, no Ollama needed!

### What You Get

- 💬 **AI Therapist** - Professional therapy techniques (CBT/DBT)
- 🎤 **Voice Interaction** - Speak naturally, get voice responses
- 🎨 **Animated Companion** - Cute blob character that reacts
- 🧠 **Smart Emotion Detection** - Understands how you feel
- 🆓 **Completely FREE** - No subscriptions, no limits
- 🔒 **100% Private** - All data stays on your computer

---

## System Requirements

- **OS:** Windows 7 or newer (Mac/Linux coming soon)
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 200MB free space
- **Browser:** Chrome, Edge, or any modern browser
- **Internet:** Optional (basic mode works offline!)

---

## AI Modes

Your app automatically chooses the best AI based on what's available:

### 1. Free Cloud AI (Best Quality - Internet Required)

**Groq API** (Recommended)
- ✅ FREE 30 requests per minute
- ✅ Llama 3.3 70B model
- ✅ No credit card needed
- ✅ Sign up: https://console.groq.com/keys

**Together.ai**
- ✅ FREE $25 credit on signup
- ✅ Multiple models available
- ✅ Sign up: https://api.together.xyz/

### 2. Local AI (Fully Private - Requires Ollama)

If you want 100% offline AI:
1. Install Ollama: https://ollama.com
2. Run: `ollama pull gemma2:2b`
3. Restart EmoSupport

### 3. Built-in Responses (Always Available)

- ✅ Works offline
- ✅ No setup needed
- ✅ Evidence-based therapy responses
- ✅ Adapts to your emotions
- ✅ **This is what runs by default!**

---

## Getting Better AI (Optional)

Want the best AI responses? Get a free Groq API key!

**Step 1:** Go to https://console.groq.com/keys

**Step 2:** Sign up (free, no credit card)

**Step 3:** Create API key

**Step 4:** Add to EmoSupport
   - Create a file called `.env` next to `EmoSupport.exe`
   - Add this line:
     ```
     GROQ_API_KEY=your_key_here
     ```
   - Restart EmoSupport

That's it! Now you have enterprise-quality AI for free!

---

## Features

### Text Chat
- Type your thoughts and feelings
- Get empathetic, therapeutic responses
- CBT techniques to challenge negative thoughts
- DBT skills for emotion regulation
- Coping strategies and exercises

### Voice Therapy
1. Click "Start Talking" 🎤
2. Speak naturally about your feelings
3. AI responds with appropriate voice tone
4. **Interrupt anytime** - just start speaking!

### Animated Companion
- Organic blob character
- Shows when listening (teal) vs speaking (purple)
- Facial expressions and emotions
- Audio-reactive animations
- Breathing and thinking states

### Therapeutic Techniques
- **Thought Challenging** - Question negative beliefs
- **Behavioral Activation** - Get moving again
- **Mindfulness** - Stay present
- **Grounding** - 5-4-3-2-1 technique
- **Breathing Exercises** - 4-7-8 method
- **Crisis Support** - Immediate resources

---

## Privacy & Security

### Your Data is Private
- ✅ All conversations stored locally on your PC
- ✅ No cloud storage
- ✅ No account required
- ✅ No tracking or analytics
- ✅ You own your data

### AI Processing
- **Cloud AI:** Messages sent to API (encrypted HTTPS)
- **Local AI:** Everything stays on your computer
- **Built-in:** No internet needed at all

### Delete Your Data
Just delete the `data` folder next to `EmoSupport.exe`

---

## Troubleshooting

### App Won't Start
- **Antivirus blocking?** Add exception for EmoSupport.exe
- **Port in use?** Close other apps using port 8000
- **Try:** Right-click > Run as Administrator

### Browser Doesn't Open
- Manually open: `http://localhost:8000`
- Check firewall isn't blocking

### AI Not Responding
- **Check internet** if using cloud AI
- **Verify API key** in .env file
- **Built-in mode** always works (may be less advanced)

### Voice Not Working
- **Use Chrome or Edge** (best Web Speech API support)
- **Allow microphone** when prompted
- **Use headphones** to prevent echo
- **Check volume** settings

### Slow Responses
- **Cloud AI:** Check internet speed
- **Local AI:** Needs good CPU/GPU
- **Built-in:** Instant responses

---

## Updating

### How to Update
1. Download new version
2. Replace old `EmoSupport.exe`
3. Your data is preserved (in `data` folder)

### Check for Updates
- GitHub Releases: [Your Repo]/releases
- Auto-update coming soon!

---

## Advanced Configuration

### Config File (.env)

Create `.env` file next to `EmoSupport.exe`:

```env
# Free AI APIs
GROQ_API_KEY=your_groq_key
TOGETHER_API_KEY=your_together_key

# Local Ollama (optional)
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=gemma2:2b

# App Settings
APP_TITLE=My Therapy Companion
SESSION_TIMEOUT=7200
```

### Custom Port

Run from command line:
```bash
EmoSupport.exe --port 8080
```

---

## Uninstalling

### Simple Uninstall
1. Delete `EmoSupport.exe`
2. Delete `data` folder (removes your conversations)
3. Done!

### Complete Cleanup
Also delete:
- `.env` file (if you created one)
- `emosup.db` (database file)

---

## Support

### Need Help?
- 📖 Full Documentation: BUILD_STANDALONE_APP.md
- 🐛 Report Issues: [GitHub Issues]
- 💬 Community: [Discord/Forum]
- 📧 Email: support@emosup.app

### In Crisis?
This app is NOT a replacement for professional help.

**Immediate Support:**
- 🆘 National Suicide Prevention: **988** (US)
- 📱 Crisis Text Line: Text **HOME** to **741741**
- 🌍 International: https://www.iasp.info/resources/Crisis_Centres/
- 🚨 Emergency: **911** or local emergency services

---

## Credits

**Built with:**
- Python + Flask (Backend)
- React + Next.js (Frontend)
- Web Speech API (Voice)
- Free AI APIs (Groq, Together.ai, HuggingFace)
- Evidence-based therapy techniques (CBT/DBT)
- Love for mental health 💜

**Therapeutic Approaches:**
- Cognitive Behavioral Therapy (Aaron Beck)
- Dialectical Behavior Therapy (Marsha Linehan)
- Motivational Interviewing (Miller & Rollnick)
- Person-Centered Therapy (Carl Rogers)

---

## License

Free for personal use. See LICENSE file for details.

---

## Disclaimer

⚠️ **IMPORTANT:** This is an AI companion for emotional support, NOT a licensed therapist. It does not replace professional mental health care. If you're experiencing a mental health crisis, please contact emergency services or a crisis helpline immediately.

**What it IS:**
- ✅ Supportive companion
- ✅ Evidence-based coping techniques
- ✅ Emotion validation and empathy
- ✅ Crisis resource provider

**What it's NOT:**
- ❌ Medical diagnosis
- ❌ Professional therapy
- ❌ Emergency service
- ❌ Medication prescription

---

**Take care of yourself. You deserve support. 💜**

**Download:** [Latest Release]

**Star on GitHub:** [Repo Link]

**Share with someone who needs support! 🌟**
