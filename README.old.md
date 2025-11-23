# Emotional Support Companion - AI Chatbot

An empathetic AI-powered emotional support chatbot built with LangChain, Ollama (Gemma 4B), and Streamlit. This application provides 24/7 emotional support, mood tracking, and coping strategies to help reduce loneliness and promote mental well-being.

## Features

### Core Features
- **24/7 Emotional Support**: AI-powered empathetic conversations using Gemma 4B model
- **Emotion Detection**: Real-time emotion analysis using NLP and sentiment analysis
- **User Authentication**: Secure login system with encrypted password storage
- **Mood Tracking**: Track and visualize your emotional patterns over time
- **Coping Strategies**: Personalized suggestions based on detected emotions
- **Conversation History**: Save and review past conversations
- **Crisis Detection**: Identifies crisis situations and provides emergency resources

### Technical Features
- Built with LangChain for advanced conversation management
- Ollama integration for local LLM inference (Gemma 4B)
- SQLite database for data persistence
- Beautiful Streamlit UI with interactive visualizations
- Sentiment analysis with TextBlob
- Secure password hashing with bcrypt

## Installation

### Prerequisites
- Python 3.8 or higher
- Ollama installed on your system
- At least 8GB RAM (for Gemma 4B model)

### Step 1: Install Ollama

Download and install Ollama from https://ollama.com

### Step 2: Pull Gemma Model

```bash
ollama pull gemma2:2b
```

Note: You can also use other models like `gemma2:9b` or `llama3.2` by updating the MODEL_NAME in `.env`

### Step 3: Clone/Download Project

```bash
cd C:\Users\hp\OneDrive\Desktop\emosup
```

### Step 4: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

Note: If you encounter issues with `sqlite3`, it usually comes pre-installed with Python. Remove it from requirements.txt if needed.

### Step 6: Download TextBlob Corpora

```bash
python -m textblob.download_corpora
```

### Step 7: Configure Environment

Copy `.env.example` to `.env` and modify if needed:

```bash
copy .env.example .env
```

Default configuration:
```
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=gemma2:2b
APP_TITLE=Emotional Support Companion
```

## Running the Application

**👉 For detailed step-by-step instructions, see [START_GUIDE.md](START_GUIDE.md)**

### Quick Start (Streamlit App)

1. Start Ollama: `ollama serve`
2. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
3. Run: `streamlit run app.py`
4. Open browser to: `http://localhost:8501`

### Quick Start (Next.js Frontend)

1. Terminal 1: `ollama serve`
2. Terminal 2: `venv\Scripts\activate` then `python api_server.py`
3. Terminal 3: `npm run dev`
4. Open browser to: `http://localhost:3000`

For complete instructions, troubleshooting, and details about both interfaces, see [START_GUIDE.md](START_GUIDE.md).

## Usage Guide

### First Time Setup

1. **Sign Up**: Create a new account with username, email, and password
2. **Login**: Use your credentials to log in
3. **Start Chatting**: Begin your first conversation

### Using the Chat

1. Type your thoughts and feelings in the chat input
2. The AI will respond with empathy and understanding
3. Emotions are automatically detected and displayed
4. Relevant coping strategies are suggested when needed

### Mood Tracking

1. Navigate to "📊 Mood Tracker" from the sidebar
2. View your emotional patterns over time
3. Analyze emotion distribution and trends
4. Track your progress with statistics

### Coping Resources

1. Access "🌟 Coping Resources" for self-care tips
2. Browse strategies organized by emotion
3. Try breathing exercises for immediate relief
4. Find crisis hotlines if needed

### Profile Management

1. View your profile information in "⚙️ Profile"
2. Access conversation history
3. Load previous conversations to continue

## Project Structure

```
emosup/
├── app.py                  # Main Streamlit application
├── chatbot.py              # Core chatbot logic with LangChain
├── emotion_analyzer.py     # Emotion detection and sentiment analysis
├── database.py             # SQLite database management
├── config.py               # Configuration and settings
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
└── data/                   # Database and user data (auto-created)
    ├── emosup.db           # SQLite database
    └── sessions/           # Session files
```

## Database Schema

### Users Table
- user_id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- full_name
- created_at
- last_login

### Conversations Table
- conversation_id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- started_at
- ended_at

### Messages Table
- message_id (PRIMARY KEY)
- conversation_id (FOREIGN KEY)
- role (user/assistant)
- content
- emotion
- sentiment_polarity
- sentiment_subjectivity
- timestamp

### Mood Logs Table
- log_id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- mood_score
- primary_emotion
- notes
- logged_at

## Customization

### Using Different Models

Edit `.env` file:
```
MODEL_NAME=gemma2:9b  # or llama3.2, mistral, etc.
```

### Adjusting Emotion Keywords

Edit `config.py` and modify the `EMOTION_KEYWORDS` dictionary:

```python
EMOTION_KEYWORDS = {
    "sad": ["sad", "down", "depressed", ...],
    "anxious": ["anxious", "worried", ...],
    # Add more emotions
}
```

### Adding Coping Strategies

Edit `config.py` and add to `COPING_STRATEGIES`:

```python
COPING_STRATEGIES = {
    "sad": [
        "Try taking a walk",
        # Add more strategies
    ]
}
```

## Technical Details

### LangChain Integration

The chatbot uses LangChain's:
- `Ollama` LLM wrapper for model integration
- `ConversationBufferMemory` for conversation context
- `PromptTemplate` for structured prompts
- `LLMChain` for conversation flow

### Emotion Detection

Uses a hybrid approach:
1. Keyword-based emotion detection
2. TextBlob sentiment analysis (polarity and subjectivity)
3. Fallback to sentiment-based emotion classification

### Security

- Passwords are hashed using bcrypt
- SQL injection prevention with parameterized queries
- Session-based authentication
- No sensitive data in plain text

## Troubleshooting

### Ollama Connection Error

**Problem**: "Failed to connect to Ollama"

**Solution**:
1. Ensure Ollama is running: `ollama serve`
2. Check if model is installed: `ollama list`
3. Verify OLLAMA_BASE_URL in `.env`

### Model Not Found

**Problem**: Model 'gemma2:2b' not found

**Solution**:
```bash
ollama pull gemma2:2b
```

### Slow Responses

**Problem**: Chatbot takes too long to respond

**Solution**:
1. Use a smaller model (gemma2:2b instead of gemma2:9b)
2. Ensure sufficient RAM available
3. Close other applications

### TextBlob Import Error

**Problem**: "No module named 'textblob'"

**Solution**:
```bash
pip install textblob
python -m textblob.download_corpora
```

### Database Locked

**Problem**: "Database is locked"

**Solution**:
1. Close all instances of the app
2. Delete `data/emosup.db.lock` if it exists
3. Restart the application

## Project Background

This project addresses the growing issue of loneliness and lack of accessible emotional support systems. It aligns with multiple UN Sustainable Development Goals:

- **SDG 3**: Good Health and Well-Being
- **SDG 4**: Quality Education (mental health awareness)
- **SDG 10**: Reduced Inequalities (accessible support)
- **SDG 16**: Peace, Justice, and Strong Institutions

## Methodology

1. **Data Collection**: User inputs and emotional responses
2. **Data Preprocessing**: Text cleaning and normalization
3. **Model Development**: LangChain + Ollama integration
4. **Emotion Analysis**: Hybrid keyword + sentiment approach
5. **Chatbot Framework**: Streamlit-based interactive UI
6. **Integration**: Database, authentication, and analytics

## Expected Results

- Successful emotion identification using NLP
- Empathetic and context-aware responses
- Measurable improvement in user emotional well-being
- High user engagement and satisfaction
- Safe, non-judgmental platform for expression

## Limitations

- Not a replacement for professional mental health care
- AI may occasionally produce imperfect responses
- Requires internet connection for model inference
- Limited to English language support
- Emotion detection based on keywords may not always be accurate

## Future Enhancements

- Multi-language support
- Voice input/output capabilities
- Integration with mental health professionals
- Mobile application
- Group support features
- Advanced emotion recognition using ML models
- Personalized therapy techniques
- Integration with wearables for mood tracking

## References

1. "Therapeutic Potential of Social Chatbots in Alleviating Loneliness and Social Anxiety" (JMIR, 2025)
2. "AI Companions Reduce Loneliness" (Journal of Consumer Research, 2025)
3. "AI Chatbots for Psychological Health for Health Professionals" (JMIR Human Factors, 2025)

## Contributing

This is a mini-project for educational purposes. Contributions and suggestions are welcome!

## Disclaimer

This chatbot is designed for emotional support and companionship. It is NOT a substitute for professional mental health services. If you are experiencing a mental health crisis, please contact:

- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- Emergency Services: 911 or your local emergency number

## License

This project is created for academic purposes as part of a CSE mini-project.

## Contact

For questions or feedback about this project, please refer to your project documentation or contact your project advisor.

---

**Built with ❤️ using LangChain, Ollama, and Streamlit**
