# Quick Start Guide

> **For comprehensive step-by-step instructions, see [START_GUIDE.md](START_GUIDE.md)**

## 5-Minute Setup

### 1. Install Ollama
Download from: https://ollama.com

### 2. Install Gemma Model
```bash
ollama pull gemma2:2b
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

### 4. Create Environment File
```bash
copy .env.example .env
```

### 5. Run the Application
```bash
# Terminal 1: Start Ollama (if not auto-started)
ollama serve

# Terminal 2: Start the app
streamlit run app.py
```

### 6. Create Account
- Open http://localhost:8501 in your browser
- Click "Sign Up" tab
- Create your account
- Login and start chatting!

## Testing the App

### Test User Credentials (for development)
You can create a test account:
- Username: testuser
- Email: test@example.com
- Password: test123

### Try These Prompts
1. "I'm feeling really lonely today"
2. "I'm anxious about my exams"
3. "I had a great day!"
4. "I feel overwhelmed with everything"

## Common Issues

### "Failed to connect to Ollama"
```bash
# Make sure Ollama is running
ollama serve

# Check if model exists
ollama list
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### App won't start
```bash
# Try with explicit path
python -m streamlit run app.py
```

## Features to Explore

1. **Chat**: Talk about your feelings
2. **Mood Tracker**: See your emotional patterns
3. **Coping Resources**: Get helpful strategies
4. **Profile**: View conversation history

## Need Help?

- **For complete startup instructions**: See [START_GUIDE.md](START_GUIDE.md)
- **For detailed documentation**: See [README.md](README.md)
- **For troubleshooting**: See [START_GUIDE.md](START_GUIDE.md) troubleshooting section
