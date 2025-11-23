# How to Start the Emotional Support Companion App

This guide provides step-by-step instructions for starting the application. The app has **two interfaces** you can use:

1. **Streamlit App** (Full-featured with authentication, mood tracking, etc.)
2. **Next.js Frontend** (Simple chatbot interface that connects to Flask API)

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Python 3.8+** installed and added to PATH
- [ ] **Node.js 18+** installed (for Next.js frontend)
- [ ] **Ollama** installed and running
- [ ] **Gemma 2B model** downloaded via Ollama
- [ ] At least **8GB RAM** available
- [ ] Stable internet connection (for initial setup)

---

## Part 1: Initial Setup (One-Time Only)

### Step 1: Install Ollama

1. Download Ollama from: https://ollama.com
2. Install it following the platform-specific instructions
3. Verify installation:
   ```bash
   ollama --version
   ```

### Step 2: Download the AI Model

Open a terminal and run:
```bash
ollama pull gemma2:2b
```

This downloads approximately 1.5GB. Wait for completion.

Verify the model is installed:
```bash
ollama list
```

You should see `gemma2:2b` in the list.

### Step 3: Install Python Dependencies

1. Navigate to the project directory:
   ```bash
   cd C:\Users\hp\OneDrive\Desktop\emosup
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Download TextBlob corpora:
   ```bash
   python -m textblob.download_corpora
   ```

### Step 4: Install Node.js Dependencies (For Next.js Frontend)

If you want to use the Next.js frontend:

1. Navigate to the project directory
2. Install dependencies:
   ```bash
   npm install
   ```

### Step 5: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
   (or `cp .env.example .env` on macOS/Linux)

2. The default `.env` file contains:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   MODEL_NAME=gemma2:2b
   APP_TITLE=Emotional Support Companion
   ```

   You typically don't need to change these unless Ollama is running on a different port.

### Step 6: Verify Setup

Run the test script to verify everything is working:
```bash
python test_setup.py
```

All tests should pass. If any fail, fix the issues before proceeding.

---

## Part 2: Starting the Application

You can run either the Streamlit app OR the Next.js frontend. Choose based on your needs:

### Option A: Streamlit App (Full-Featured)

**Best for:** Full experience with authentication, mood tracking, analytics, and all features.

#### Step 1: Start Ollama (if not already running)

Ollama usually starts automatically, but if needed:
```bash
ollama serve
```

Keep this terminal open. You should see: `Ollama is running on http://localhost:11434`

#### Step 2: Activate Virtual Environment

```bash
venv\Scripts\activate
```
(or `source venv/bin/activate` on macOS/Linux)

#### Step 3: Start Streamlit App

```bash
streamlit run app.py
```

#### Step 4: Access the App

The app will automatically open in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, navigate to the URL manually.

#### Step 5: Create an Account

1. Click on the **"Sign Up"** tab
2. Fill in:
   - Username (must be unique)
   - Email (must be unique)
   - Full Name (optional)
   - Password (minimum 6 characters)
   - Confirm Password
3. Click **"Sign Up"**
4. Switch to **"Login"** tab
5. Enter your credentials
6. Click **"Login"**

#### Step 6: Start Using the App

Once logged in, you can:
- **Chat**: Navigate to "💬 Chat" and start a conversation
- **Track Mood**: View your emotional patterns in "📊 Mood Tracker"
- **Get Help**: Access coping strategies in "🌟 Coping Resources"
- **View Profile**: Check your conversation history in "⚙️ Profile"

---

### Option B: Next.js Frontend (Simple Chatbot Interface)

**Best for:** Quick, simple chatbot interface without authentication.

#### Step 1: Start Ollama (if not already running)

```bash
ollama serve
```

Keep this terminal open.

#### Step 2: Start Flask API Server

Open a **new terminal** and:

1. Navigate to the project directory
2. Activate virtual environment:
   ```bash
   venv\Scripts\activate
   ```
3. Start the Flask API server:
   ```bash
   python api_server.py
   ```

You should see:
```
Starting Flask API server on http://localhost:5000
Running on http://0.0.0.0:5000
```

**Keep this terminal open.** The API server must be running for the frontend to work.

#### Step 3: Start Next.js Development Server

Open **another new terminal** and:

1. Navigate to the project directory
2. Start the Next.js server:
   ```bash
   npm run dev
   ```

You should see:
```
- ready started server on 0.0.0.0:3000
- Local:        http://localhost:3000
```

#### Step 4: Access the App

Open your browser and navigate to:
```
http://localhost:3000
```

#### Step 5: Use the Chatbot

1. You'll see a landing page with quick prompts
2. Click "Start Chat" or select a quick prompt
3. The chatbot interface will open
4. Type your message and press Enter or click Send
5. The AI will respond with empathy and support

---

## Part 3: What Should Be Running

### For Streamlit App:
- ✅ **Ollama** service (running on port 11434)
- ✅ **Streamlit** app (running on port 8501)

### For Next.js Frontend:
- ✅ **Ollama** service (running on port 11434)
- ✅ **Flask API** server (running on port 5000)
- ✅ **Next.js** dev server (running on port 3000)

---

## Part 4: Daily Startup Routine

### Quick Start (Streamlit):

1. Open terminal
2. Activate venv: `venv\Scripts\activate`
3. Start Ollama (if not auto-running): `ollama serve`
4. Run: `streamlit run app.py`
5. Open browser to http://localhost:8501

### Quick Start (Next.js):

1. Terminal 1: `ollama serve`
2. Terminal 2: `venv\Scripts\activate` then `python api_server.py`
3. Terminal 3: `npm run dev`
4. Open browser to http://localhost:3000

---

## Troubleshooting

### Problem: "Failed to connect to Ollama"

**Solution:**
1. Make sure Ollama is running: `ollama serve`
2. Check if the model is installed: `ollama list`
3. Verify port 11434 is not blocked by firewall
4. Check `.env` file has correct `OLLAMA_BASE_URL`

### Problem: "Model 'gemma2:2b' not found"

**Solution:**
```bash
ollama pull gemma2:2b
```
Wait for the download to complete (about 1.5GB).

### Problem: "Cannot connect to API server" (Next.js)

**Solution:**
1. Make sure Flask API server is running: `python api_server.py`
2. Check if port 5000 is available (not used by another app)
3. Wait for the "Running on http://0.0.0.0:5000" message before using frontend

### Problem: "Port already in use"

**Solution:**
- For Streamlit: `streamlit run app.py --server.port 8502`
- For Flask: Edit `api_server.py` and change port 5000 to another port
- For Next.js: `npm run dev -- -p 3001`

### Problem: "Module not found" errors

**Solution:**
1. Make sure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt --upgrade`
3. Download TextBlob data: `python -m textblob.download_corpora`

### Problem: Slow responses from chatbot

**Solutions:**
- Use smaller model: `gemma2:2b` (already default)
- Close other applications to free RAM
- Ensure you have at least 8GB RAM available
- Check CPU usage - inference is CPU-intensive

### Problem: Database locked

**Solution:**
1. Close all instances of the app
2. Delete lock file if exists: `del data\emosup.db.lock` (Windows) or `rm data/emosup.db.lock` (macOS/Linux)
3. Restart the application

### Problem: Next.js won't start

**Solution:**
1. Delete `node_modules` folder: `rmdir /s node_modules` (Windows) or `rm -rf node_modules` (macOS/Linux)
2. Delete `package-lock.json`
3. Reinstall: `npm install`
4. Try again: `npm run dev`

---

## Stopping the Application

### To Stop Streamlit:
- Press `Ctrl+C` in the terminal running Streamlit

### To Stop Next.js:
- Press `Ctrl+C` in the terminal running `npm run dev`

### To Stop Flask API:
- Press `Ctrl+C` in the terminal running `python api_server.py`

### To Stop Ollama:
- Press `Ctrl+C` in the terminal running `ollama serve`
- Or close the terminal window

**Important:** Always stop services gracefully using `Ctrl+C` rather than closing terminals abruptly.

---

## Important Notes

1. **Ollama must be running** before starting either app
2. **For Next.js frontend**, both Flask API and Next.js servers must be running
3. **Virtual environment** should be activated before running Python scripts
4. **Database** is created automatically on first run in `data/emosup.db`
5. **All data is stored locally** - no data is sent to external servers (except Ollama for inference)

---

## Next Steps After Starting

1. **Create your account** (Streamlit only)
2. **Start a conversation** - try expressing your feelings
3. **Explore features**:
   - Check mood tracker after a few conversations
   - Browse coping resources
   - Review conversation history
4. **Customize** - adjust settings in profile if available

---

## Getting Help

If you encounter issues:

1. Run the test script: `python test_setup.py`
2. Check error messages in the terminal
3. Verify all prerequisites are installed
4. Ensure Ollama is running and model is downloaded
5. Check the main README.md for detailed troubleshooting

---

## Summary

**Streamlit App:**
1. Start Ollama: `ollama serve`
2. Activate venv: `venv\Scripts\activate`
3. Run: `streamlit run app.py`
4. Open: http://localhost:8501

**Next.js Frontend:**
1. Terminal 1: `ollama serve`
2. Terminal 2: `venv\Scripts\activate` → `python api_server.py`
3. Terminal 3: `npm run dev`
4. Open: http://localhost:3000

That's it! You're ready to use the Emotional Support Companion. 🎉



