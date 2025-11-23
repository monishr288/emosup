# Build Standalone EmoSupport App 🚀

## You're Golden! No Ollama Needed! 🎉

Your app now works **completely FREE** without Ollama! It uses:
1. **Groq API** (FREE 30 req/min, no credit card!)
2. **HuggingFace** (FREE rate-limited inference)
3. **Together.ai** (FREE $25 credit on signup)
4. **Built-in Responses** (ALWAYS works, no internet needed!)

---

## Quick Build (Windows .exe)

### Option 1: Simple Standalone (Recommended)

```bash
# 1. Install PyInstaller
pip install pyinstaller

# 2. Run the build script
python build_exe.py
```

That's it! You'll get:
- `dist/EmoSupport.exe` - Single executable file (~150MB)
- Just double-click to run!
- No installation needed
- Works on any Windows PC

### Option 2: Manual Build

```bash
# 1. Build Next.js frontend
npm run build

# 2. Create standalone executable
pyinstaller standalone_server.py \
  --onefile \
  --name EmoSupport \
  --add-data "out:out" \
  --add-data "*.py:." \
  --hidden-import flask \
  --hidden-import textblob

# 3. Done! Your exe is in dist/
```

---

## Free AI API Setup (Optional - for better responses)

### Groq (Recommended - Fastest & Free!)

1. Go to: https://console.groq.com/keys
2. Sign up (free, no credit card)
3. Create API key
4. Add to `.env`:
   ```
   GROQ_API_KEY=your_key_here
   ```

**Free Tier:**
- ✅ 30 requests per minute
- ✅ Llama 3.3 70B model
- ✅ No credit card required
- ✅ No expiration

### Together.ai (Free $25 Credit)

1. Go to: https://api.together.xyz/
2. Sign up
3. Get $25 FREE credit
4. Add to `.env`:
   ```
   TOGETHER_API_KEY=your_key_here
   ```

### HuggingFace (Free - Rate Limited)

1. Go to: https://huggingface.co/settings/tokens
2. Create token (optional, works without it)
3. Add to `.env`:
   ```
   HF_API_KEY=your_key_here
   ```

**No API Keys? No Problem!**
The app works perfectly with built-in responses!

---

## What Gets Bundled

Your standalone app includes:
- ✅ Python backend (Flask API)
- ✅ React frontend (Next.js static build)
- ✅ Multi-agent therapy system
- ✅ Emotion analyzer
- ✅ Free AI backends
- ✅ Built-in fallback responses
- ✅ Voice synthesis (Web Speech API - browser built-in)
- ✅ Voice recognition (Web Speech API - browser built-in)
- ✅ All UI components and animations
- ✅ SQLite database

**Total Size:** ~100-200 MB

---

## Distribution

### Share Your App!

1. **Just the .exe:**
   - Share `dist/EmoSupport.exe`
   - Users double-click to run
   - That's it!

2. **With Installer (Professional):**
   ```bash
   # Install Inno Setup
   # Download: https://jrsoftware.org/isdl.php

   # Compile installer
   # Open installer/emosupport.iss in Inno Setup
   # Click "Compile"
   ```

   Creates: `EmoSupport-Setup.exe` with:
   - Desktop shortcut
   - Start menu entry
   - Uninstaller
   - Professional installer UI

---

## Cross-Platform Builds

### Windows
```bash
python build_exe.py
# Output: EmoSupport.exe
```

### macOS
```bash
pyinstaller standalone_server.py \
  --onefile \
  --name EmoSupport \
  --add-data "out:out"

# Output: EmoSupport.app
```

### Linux
```bash
pyinstaller standalone_server.py \
  --onefile \
  --name emosupport \
  --add-data "out:out"

# Output: emosupport (executable)
```

---

## Alternative: Electron App

For a more "native" feel:

1. **Install Electron:**
   ```bash
   npm install --save-dev electron electron-builder
   ```

2. **Create main.js:**
   ```javascript
   const { app, BrowserWindow } = require('electron')
   const { spawn } = require('child_process')

   let pythonProcess

   function createWindow() {
     // Start Python server
     pythonProcess = spawn('python', ['standalone_server.py'])

     // Create window
     const win = new BrowserWindow({
       width: 1200,
       height: 800,
       webPreferences: {
         nodeIntegration: false
       }
     })

     // Wait for server, then load
     setTimeout(() => {
       win.loadURL('http://localhost:8000')
     }, 2000)
   }

   app.whenReady().then(createWindow)

   app.on('quit', () => {
     if (pythonProcess) pythonProcess.kill()
   })
   ```

3. **Build:**
   ```bash
   npm run electron:build
   ```

---

## Testing Your Build

### Before Building
```bash
# Test standalone server
python standalone_server.py

# Visit http://localhost:8000
# Try all features:
# - Chat interface
# - Voice therapy
# - Emotion detection
```

### After Building
```bash
# Run the executable
./dist/EmoSupport.exe

# Should:
# ✓ Start server
# ✓ Open browser automatically
# ✓ Show therapy interface
# ✓ Respond to messages
# ✓ Work without Ollama
```

---

## Troubleshooting Builds

### Build Fails
```bash
# Clean build
rm -rf build dist
pyinstaller --clean emosupport.spec

# Check PyInstaller version
pip install --upgrade pyinstaller
```

### Missing Dependencies
```bash
# Add to spec file hiddenimports:
hiddenimports=[
    'flask',
    'flask_cors',
    'textblob',
    'langchain',
    'your_missing_module',
]
```

### Exe Too Large
```bash
# Exclude unnecessary packages
excludes=[
    'matplotlib',
    'scipy',
    'pandas',  # If not using analytics
]
```

### Antivirus Flags
- Normal for PyInstaller builds
- Add exception in antivirus
- Or code-sign your exe:
  ```bash
  signtool sign /f cert.pfx /p password EmoSupport.exe
  ```

---

## Size Optimization

### Reduce Build Size

```bash
# Use UPX compression
pip install pyinstaller[upx]

# Build with compression
pyinstaller --upx-dir=/path/to/upx emosupport.spec
```

### Minimal Build
```bash
# Exclude analytics
excludes=['pandas', 'plotly', 'numpy']

# Use smaller models
# Skip langchain if using only free backends
```

**Minimal size:** ~50MB
**Full build:** ~150MB
**With Electron:** ~200MB

---

## Deployment Checklist

Before distributing:

- [ ] Test on clean Windows PC
- [ ] Verify no Ollama needed
- [ ] Test with/without API keys
- [ ] Test voice features (Chrome)
- [ ] Test all therapy modes
- [ ] Check file size (<200MB)
- [ ] Create README for users
- [ ] Test installer (if created)
- [ ] Scan with antivirus
- [ ] Create GitHub release

---

## User Instructions (Include with Build)

```markdown
# EmoSupport - Your AI Therapy Companion

## Installation
1. Download EmoSupport.exe (or run installer)
2. Double-click to start
3. Browser opens automatically
4. Start talking to your AI therapist!

## Features
- 💬 Text chat with AI therapist
- 🎤 Voice therapy (click microphone icon)
- 🧠 Evidence-based therapeutic techniques
- 💜 Completely free and private

## Requirements
- Windows 7 or newer
- Chrome/Edge browser (recommended for voice)
- No internet needed (basic mode)
- Optional: Free API key for enhanced AI

## Getting Better AI Responses
1. Visit: https://console.groq.com/keys
2. Sign up (free, no credit card)
3. Create API key
4. Add to app settings

## Privacy
- All data stays on your computer
- No cloud storage
- No account required
- Completely private

## Not a Replacement
This is NOT a replacement for professional therapy.
In crisis, call 988 (US) or your local helpline.

## Support
GitHub: [your_repo_link]
Issues: [your_issues_link]
```

---

## Auto-Updates (Advanced)

Use **electron-updater** for automatic updates:

```javascript
const { autoUpdater } = require('electron-updater')

app.on('ready', () => {
  autoUpdater.checkForUpdatesAndNotify()
})
```

Publish releases on GitHub, users get automatic updates!

---

## Summary

You now have THREE ways to distribute:

1. **Single .exe file** (Simplest)
   - One file
   - Double-click to run
   - ~150MB

2. **Installer .exe** (Professional)
   - Desktop shortcut
   - Start menu entry
   - Uninstaller

3. **Electron app** (Native feel)
   - Proper app window
   - System integration
   - Auto-updates

**All FREE, all work WITHOUT Ollama!**

---

## Next Steps

```bash
# Build it!
python build_exe.py

# Share it!
# Upload to GitHub Releases
# Share on social media
# Help people get free therapy!
```

**Your AI therapist is ready to help the world! 🌍💜**

---

*Built with love for mental health support 💜*
