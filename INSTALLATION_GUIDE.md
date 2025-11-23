# Complete Installation Guide

## Prerequisites Checklist

Before you begin, make sure you have:
- [ ] Windows 10/11, macOS, or Linux
- [ ] At least 8GB RAM
- [ ] 10GB free disk space
- [ ] Internet connection
- [ ] Administrator/sudo privileges

---

## Step-by-Step Installation

### Step 1: Install Python

1. Download Python 3.8 or higher from https://www.python.org/downloads/
2. During installation:
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

### Step 2: Install Ollama

#### Windows:
1. Download from https://ollama.com/download/windows
2. Run the installer
3. Verify by opening Command Prompt:
   ```bash
   ollama --version
   ```

#### macOS:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 3: Install Gemma Model

Open terminal/command prompt:
```bash
ollama pull gemma2:2b
```

This will download approximately 1.5GB of data. Wait for completion.

To verify:
```bash
ollama list
```

You should see `gemma2:2b` in the list.

### Step 4: Set Up Project

#### Option A: Automated Setup (Windows)

1. Navigate to project directory:
   ```bash
   cd C:\Users\hp\OneDrive\Desktop\emosup
   ```

2. Run setup script:
   ```bash
   setup.bat
   ```

3. Follow on-screen instructions

#### Option B: Manual Setup

1. Navigate to project directory:
   ```bash
   cd C:\Users\hp\OneDrive\Desktop\emosup
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Download TextBlob corpora:
   ```bash
   python -m textblob.download_corpora
   ```

### Step 5: Configure Environment

1. Copy example environment file:
   ```bash
   copy .env.example .env
   ```

2. (Optional) Edit `.env` if needed:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   MODEL_NAME=gemma2:2b
   APP_TITLE=Emotional Support Companion
   ```

### Step 6: Test Setup

Run the test script:
```bash
python test_setup.py
```

All tests should pass. If any fail, refer to the error messages.

---

## Running the Application

### Option 1: Using Run Script (Windows)

Double-click `run.bat` or in terminal:
```bash
run.bat
```

### Option 2: Manual Start

1. Activate virtual environment (if not already):
   ```bash
   venv\Scripts\activate
   ```

2. Run the application:
   ```bash
   streamlit run app.py
   ```

3. The app will automatically open in your browser at:
   ```
   http://localhost:8501
   ```

---

## First Time Usage

### Create Account

1. Click on **"Sign Up"** tab
2. Fill in:
   - Username (unique)
   - Email (unique)
   - Full Name (optional)
   - Password (minimum 6 characters)
   - Confirm Password
3. Click **"Sign Up"**
4. Switch to **"Login"** tab
5. Enter your credentials
6. Click **"Login"**

### Start Chatting

1. You'll see the chat interface
2. Type your message in the input box at the bottom
3. Press Enter or click Send
4. The AI will respond with empathy and understanding
5. Your emotions will be automatically detected

---

## Troubleshooting

### Issue: "Python not found"

**Solution:**
- Reinstall Python with "Add to PATH" checked
- Or manually add Python to PATH
- Restart terminal after installation

### Issue: "Ollama connection failed"

**Solution:**
1. Start Ollama manually:
   ```bash
   ollama serve
   ```
2. Verify it's running:
   ```bash
   ollama list
   ```
3. Check firewall isn't blocking port 11434

### Issue: "Model not found"

**Solution:**
```bash
ollama pull gemma2:2b
```

Wait for download to complete.

### Issue: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "TextBlob corpora not found"

**Solution:**
```bash
python -m textblob.download_corpora
```

### Issue: "Port 8501 already in use"

**Solution:**
1. Stop any running Streamlit apps
2. Or specify different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```

### Issue: Slow responses

**Solutions:**
- Use smaller model: `gemma2:2b` instead of `gemma2:9b`
- Close other applications to free RAM
- Check CPU/RAM usage

### Issue: Database locked

**Solution:**
1. Close all instances of the app
2. Delete lock file if exists:
   ```bash
   del data\emosup.db.lock
   ```
3. Restart application

---

## Updating the Application

### Update Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Update Ollama Models

```bash
ollama pull gemma2:2b
```

---

## Uninstallation

### Remove Virtual Environment

```bash
rmdir /s venv
```

### Remove Database (Caution: Deletes all data)

```bash
rmdir /s data
```

### Uninstall Ollama

**Windows:**
- Use "Add or Remove Programs"
- Search for "Ollama"
- Click Uninstall

**macOS/Linux:**
```bash
sudo rm -rf /usr/local/bin/ollama
```

---

## Advanced Configuration

### Using Different Models

Edit `.env`:
```
MODEL_NAME=gemma2:9b
```

Available models:
- `gemma2:2b` (fastest, 1.5GB)
- `gemma2:9b` (better quality, 5GB)
- `llama3.2` (alternative)
- `mistral` (alternative)

Pull the model:
```bash
ollama pull gemma2:9b
```

### Changing Port

```bash
streamlit run app.py --server.port 8080
```

### Running on Network

```bash
streamlit run app.py --server.address 0.0.0.0
```

Access from other devices: `http://YOUR_IP:8501`

---

## System Requirements

### Minimum:
- CPU: 2 cores
- RAM: 8GB
- Storage: 10GB free
- OS: Windows 10, macOS 10.15, Ubuntu 20.04

### Recommended:
- CPU: 4+ cores
- RAM: 16GB
- Storage: 20GB free
- OS: Latest versions

---

## Security Notes

- Never share your `.env` file
- Keep your password secure
- Database is stored locally
- All data remains on your machine
- No data is sent to external servers (except Ollama for inference)

---

## Getting Help

### Documentation
- `README.md` - Full project documentation
- `QUICKSTART.md` - Quick start guide
- `PROJECT_SUMMARY.md` - Project overview

### Testing
```bash
python test_setup.py
```

### Check Logs
If errors occur, check Streamlit logs in terminal output.

---

## Performance Tips

1. **Use appropriate model size**
   - `gemma2:2b` for speed
   - `gemma2:9b` for quality

2. **Close unused applications**
   - Free up RAM for the model

3. **Use SSD if available**
   - Faster model loading

4. **Limit conversation length**
   - Start new conversation if responses slow down

---

## Next Steps

After successful installation:

1. ✅ Create your account
2. ✅ Explore the chat interface
3. ✅ Check mood tracker after a few conversations
4. ✅ Browse coping resources
5. ✅ Customize your profile

Enjoy using the Emotional Support Companion!

---

## Support

For issues or questions:
1. Check this guide first
2. Run `python test_setup.py`
3. Review error messages carefully
4. Check documentation files

---

**Last Updated**: 2025
**Version**: 1.0
