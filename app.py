"""
Main Streamlit application for Emotional Support Chatbot
"""
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from chatbot import EmotionalSupportChatbot
from emotion_analyzer import EmotionAnalyzer
from database import Database
import config

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E3F2FD;
        margin-left: 2rem;
    }
    .assistant-message {
        background-color: #F1F8E9;
        margin-right: 2rem;
    }
    .emotion-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'emotion_analyzer' not in st.session_state:
        st.session_state.emotion_analyzer = EmotionAnalyzer()
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'current_conversation_id' not in st.session_state:
        st.session_state.current_conversation_id = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []


def login_page():
    """Display login/signup page"""
    st.markdown('<div class="main-header">💚 Emotional Support Companion</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your 24/7 empathetic AI friend</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Welcome Back")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if username and password:
                    user_data = st.session_state.db.authenticate_user(username, password)
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")

    with tab2:
        st.subheader("Create New Account")
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email Address")
            new_full_name = st.text_input("Full Name (Optional)")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_signup = st.form_submit_button("Sign Up")

            if submit_signup:
                if not all([new_username, new_email, new_password, confirm_password]):
                    st.warning("Please fill in all required fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    user_id = st.session_state.db.create_user(
                        new_username, new_email, new_password, new_full_name
                    )
                    if user_id:
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username or email already exists")


def chat_interface():
    """Main chat interface"""
    st.title("💬 Chat with Your Support Companion")

    # Initialize chatbot if not already done
    if st.session_state.chatbot is None:
        try:
            st.session_state.chatbot = EmotionalSupportChatbot()
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {str(e)}")
            st.info("Please make sure Ollama is running with the Gemma model installed.")
            st.code("ollama pull gemma2:2b")
            return

    # Create new conversation if needed
    if st.session_state.current_conversation_id is None:
        st.session_state.current_conversation_id = st.session_state.db.create_conversation(
            st.session_state.user_data['user_id']
        )

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("emotion"):
                st.caption(f"Detected emotion: {message['emotion']}")

    # Chat input
    if prompt := st.chat_input("Share what's on your mind..."):
        # Analyze user input
        analysis = st.session_state.emotion_analyzer.analyze_text(prompt)

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "emotion": analysis["primary_emotion"]
        })

        # Save to database
        st.session_state.db.save_message(
            st.session_state.current_conversation_id,
            "user",
            prompt,
            analysis["primary_emotion"],
            analysis["sentiment"]["polarity"],
            analysis["sentiment"]["subjectivity"]
        )

        # Log mood
        st.session_state.db.log_mood(
            st.session_state.user_data['user_id'],
            analysis["sentiment"]["polarity"],
            analysis["primary_emotion"]
        )

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            st.caption(f"Detected emotion: {analysis['primary_emotion']}")

        # Get chatbot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = st.session_state.chatbot.get_response(prompt)
                response = response_data["response"]

                st.write(response)

                # Add coping suggestion if applicable
                if analysis["primary_emotion"] != "happy" and analysis["primary_emotion"] != "neutral":
                    with st.expander("💡 Coping Suggestion"):
                        st.write(analysis["coping_suggestion"])

        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        # Save assistant message to database
        st.session_state.db.save_message(
            st.session_state.current_conversation_id,
            "assistant",
            response
        )

        st.rerun()

    # Clear conversation button
    if st.button("Start New Conversation"):
        st.session_state.messages = []
        st.session_state.chatbot.reset_conversation()
        st.session_state.current_conversation_id = st.session_state.db.create_conversation(
            st.session_state.user_data['user_id']
        )
        st.rerun()


def mood_tracker():
    """Mood tracking and analytics page"""
    st.title("📊 Mood Tracker & Analytics")

    user_id = st.session_state.user_data['user_id']

    # Time period selector
    days = st.selectbox("Time Period", [7, 14, 30, 60, 90], index=2)

    # Get mood history
    mood_history = st.session_state.db.get_mood_history(user_id, days)

    if mood_history:
        # Convert to DataFrame
        df = pd.DataFrame(mood_history)
        df['logged_at'] = pd.to_datetime(df['logged_at'])

        # Mood timeline chart
        st.subheader("Mood Timeline")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['logged_at'],
            y=df['mood_score'],
            mode='lines+markers',
            name='Mood Score',
            line=dict(color='#4CAF50', width=2),
            marker=dict(size=8)
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Mood Score",
            yaxis=dict(range=[-1, 1]),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Emotion distribution
        st.subheader("Emotion Distribution")
        emotion_stats = st.session_state.db.get_emotion_statistics(user_id, days)

        if emotion_stats:
            fig = px.pie(
                values=list(emotion_stats.values()),
                names=list(emotion_stats.keys()),
                title="Your Emotional Patterns"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_mood = df['mood_score'].mean()
            st.metric("Average Mood", f"{avg_mood:.2f}")
        with col2:
            total_entries = len(df)
            st.metric("Total Entries", total_entries)
        with col3:
            if len(df) > 1:
                trend = df['mood_score'].iloc[-1] - df['mood_score'].iloc[0]
                st.metric("Trend", f"{trend:.2f}", delta=f"{trend:.2f}")

    else:
        st.info("Start chatting to build your mood history!")


def coping_resources():
    """Coping strategies and resources page"""
    st.title("🌟 Coping Resources & Self-Care")

    st.markdown("""
    Here are some helpful coping strategies and resources to support your emotional well-being.
    """)

    # Coping strategies by emotion
    st.subheader("Coping Strategies")

    for emotion, strategies in config.COPING_STRATEGIES.items():
        with st.expander(f"💚 Feeling {emotion.title()}?"):
            for strategy in strategies:
                st.markdown(f"- {strategy}")

    st.divider()

    # Breathing exercise
    st.subheader("🫁 Quick Breathing Exercise")
    st.markdown("""
    **4-7-8 Breathing Technique:**
    1. Breathe in through your nose for 4 counts
    2. Hold your breath for 7 counts
    3. Exhale completely through your mouth for 8 counts
    4. Repeat 3-4 times

    This exercise can help reduce anxiety and promote relaxation.
    """)

    st.divider()

    # Emergency resources
    st.subheader("🆘 Crisis Resources")
    st.error("""
    **If you're in crisis, please reach out:**
    - National Suicide Prevention Lifeline: **988** (US)
    - Crisis Text Line: Text **HOME** to **741741**
    - International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
    - Emergency Services: **911** (US) or your local emergency number
    """)


def profile_settings():
    """User profile and settings page"""
    st.title("⚙️ Profile & Settings")

    user_data = st.session_state.user_data

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Profile Information")
        st.write(f"**Username:** {user_data['username']}")
        st.write(f"**Email:** {user_data['email']}")
        if user_data.get('full_name'):
            st.write(f"**Name:** {user_data['full_name']}")
        st.write(f"**Member Since:** {user_data['created_at'][:10]}")

    with col2:
        st.subheader("Conversation History")
        conversations = st.session_state.db.get_user_conversations(user_data['user_id'])

        if conversations:
            for conv in conversations:
                with st.expander(f"Conversation on {conv['started_at'][:16]}"):
                    st.write(f"Messages: {conv['message_count']}")
                    if st.button(f"Load Conversation", key=f"load_{conv['conversation_id']}"):
                        # Load conversation
                        messages = st.session_state.db.get_conversation_history(conv['conversation_id'])
                        st.session_state.messages = [
                            {"role": msg['role'], "content": msg['content'], "emotion": msg['emotion']}
                            for msg in messages
                        ]
                        st.session_state.current_conversation_id = conv['conversation_id']
                        st.success("Conversation loaded!")
        else:
            st.info("No conversation history yet. Start chatting!")


def main():
    """Main application"""
    init_session_state()

    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.title("Navigation")
            st.write(f"Welcome, **{st.session_state.user_data['username']}**!")

            page = st.radio(
                "Go to",
                ["💬 Chat", "📊 Mood Tracker", "🌟 Coping Resources", "⚙️ Profile"],
                label_visibility="collapsed"
            )

            st.divider()

            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.user_data = None
                st.session_state.chatbot = None
                st.session_state.current_conversation_id = None
                st.session_state.messages = []
                st.rerun()

        # Display selected page
        if page == "💬 Chat":
            chat_interface()
        elif page == "📊 Mood Tracker":
            mood_tracker()
        elif page == "🌟 Coping Resources":
            coping_resources()
        elif page == "⚙️ Profile":
            profile_settings()


if __name__ == "__main__":
    main()
