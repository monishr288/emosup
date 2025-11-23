"""
Database management for user authentication and data storage
"""
import sqlite3
import bcrypt
from datetime import datetime
from typing import Optional, Dict, List, Any
import os


class Database:
    """
    SQLite database manager for the emotional support chatbot
    """

    def __init__(self, db_path: str = "data/emosup.db"):
        """
        Initialize database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_directory()
        self.conn = None
        self._connect()
        self._create_tables()

    def _ensure_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise ConnectionError(f"Failed to connect to database: {str(e)}")

    def _create_tables(self):
        """Create necessary database tables"""
        cursor = self.conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)

        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                emotion TEXT,
                sentiment_polarity REAL,
                sentiment_subjectivity REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
        """)

        # Mood tracking table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mood_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mood_score REAL NOT NULL,
                primary_emotion TEXT,
                notes TEXT,
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # User preferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                notification_enabled BOOLEAN DEFAULT 1,
                theme TEXT DEFAULT 'light',
                language TEXT DEFAULT 'en',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        self.conn.commit()

    # User Management
    def create_user(self, username: str, email: str, password: str, full_name: str = None) -> Optional[int]:
        """
        Create a new user

        Args:
            username: Username
            email: Email address
            password: Plain text password
            full_name: Full name (optional)

        Returns:
            User ID if successful, None otherwise
        """
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor = self.conn.cursor()

            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))

            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with username and password

        Args:
            username: Username
            password: Plain text password

        Returns:
            User data if authenticated, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT user_id, username, email, password_hash, full_name, created_at
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            # Update last login
            cursor.execute("""
                UPDATE users SET last_login = ? WHERE user_id = ?
            """, (datetime.now(), user['user_id']))
            self.conn.commit()

            return {
                "user_id": user['user_id'],
                "username": user['username'],
                "email": user['email'],
                "full_name": user['full_name'],
                "created_at": user['created_at']
            }

        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID

        Args:
            user_id: User ID

        Returns:
            User data if found, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT user_id, username, email, full_name, created_at, last_login
            FROM users
            WHERE user_id = ?
        """, (user_id,))

        user = cursor.fetchone()
        if user:
            return dict(user)
        return None

    # Conversation Management
    def create_conversation(self, user_id: int) -> int:
        """
        Create a new conversation

        Args:
            user_id: User ID

        Returns:
            Conversation ID
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (user_id)
            VALUES (?)
        """, (user_id,))
        self.conn.commit()
        return cursor.lastrowid

    def save_message(self, conversation_id: int, role: str, content: str,
                    emotion: str = None, sentiment_polarity: float = None,
                    sentiment_subjectivity: float = None):
        """
        Save a message to the database

        Args:
            conversation_id: Conversation ID
            role: 'user' or 'assistant'
            content: Message content
            emotion: Detected emotion
            sentiment_polarity: Sentiment polarity score
            sentiment_subjectivity: Sentiment subjectivity score
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, emotion,
                                 sentiment_polarity, sentiment_subjectivity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (conversation_id, role, content, emotion, sentiment_polarity, sentiment_subjectivity))
        self.conn.commit()

    def get_conversation_history(self, conversation_id: int) -> List[Dict[str, Any]]:
        """
        Get conversation history

        Args:
            conversation_id: Conversation ID

        Returns:
            List of messages
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT message_id, role, content, emotion, sentiment_polarity,
                   sentiment_subjectivity, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        """, (conversation_id,))

        return [dict(row) for row in cursor.fetchall()]

    def get_user_conversations(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's recent conversations

        Args:
            user_id: User ID
            limit: Maximum number of conversations to return

        Returns:
            List of conversations
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.conversation_id, c.started_at, c.ended_at,
                   COUNT(m.message_id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.conversation_id = m.conversation_id
            WHERE c.user_id = ?
            GROUP BY c.conversation_id
            ORDER BY c.started_at DESC
            LIMIT ?
        """, (user_id, limit))

        return [dict(row) for row in cursor.fetchall()]

    # Mood Tracking
    def log_mood(self, user_id: int, mood_score: float, primary_emotion: str = None, notes: str = None):
        """
        Log user's mood

        Args:
            user_id: User ID
            mood_score: Mood score (-1 to 1)
            primary_emotion: Primary emotion
            notes: Additional notes
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO mood_logs (user_id, mood_score, primary_emotion, notes)
            VALUES (?, ?, ?, ?)
        """, (user_id, mood_score, primary_emotion, notes))
        self.conn.commit()

    def get_mood_history(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get user's mood history

        Args:
            user_id: User ID
            days: Number of days to retrieve

        Returns:
            List of mood logs
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT log_id, mood_score, primary_emotion, notes, logged_at
            FROM mood_logs
            WHERE user_id = ?
            AND logged_at >= datetime('now', '-' || ? || ' days')
            ORDER BY logged_at DESC
        """, (user_id, days))

        return [dict(row) for row in cursor.fetchall()]

    def get_emotion_statistics(self, user_id: int, days: int = 30) -> Dict[str, int]:
        """
        Get emotion statistics for user

        Args:
            user_id: User ID
            days: Number of days to analyze

        Returns:
            Dictionary with emotion counts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT primary_emotion, COUNT(*) as count
            FROM mood_logs
            WHERE user_id = ?
            AND logged_at >= datetime('now', '-' || ? || ' days')
            AND primary_emotion IS NOT NULL
            GROUP BY primary_emotion
            ORDER BY count DESC
        """, (user_id, days))

        return {row['primary_emotion']: row['count'] for row in cursor.fetchall()}

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
