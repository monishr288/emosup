"""
Long-Term Memory System with Supabase Cloud Storage
Tracks user progress, patterns, and therapeutic journey across sessions
"""
import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class MemoryEntry:
    """Single memory entry"""
    timestamp: str
    session_id: str
    user_id: str
    message: str
    emotion: str
    emotion_intensity: float
    therapy_mode: str
    detected_patterns: List[str]
    breakthroughs: List[str]
    concerns: List[str]


@dataclass
class UserProfile:
    """Comprehensive user profile across sessions"""
    user_id: str
    created_at: str
    total_sessions: int
    total_messages: int

    # Emotional patterns
    dominant_emotions: Dict[str, int]  # emotion -> count
    emotion_trends: List[Dict[str, Any]]  # timestamp -> emotion

    # Therapeutic progress
    identified_schemas: List[str]
    core_beliefs: List[str]
    coping_strategies_tried: List[str]
    breakthroughs: List[Dict[str, str]]

    # Behavioral patterns
    common_triggers: List[str]
    time_patterns: Dict[str, int]  # hour -> frequency
    crisis_history: List[Dict[str, str]]

    # Progress tracking
    goals: List[Dict[str, Any]]
    mood_baseline: float
    mood_trend: str  # "improving", "stable", "declining"
    therapeutic_alliance: float  # 0-1 score

    # Preferences
    preferred_frameworks: List[str]
    effective_techniques: List[str]
    preferred_communication_style: str

    # Session context
    last_session: Optional[str]
    last_topic: Optional[str]
    unresolved_issues: List[str]


class SupabaseMemoryStore:
    """
    Cloud-based memory storage using Supabase
    FREE tier: 500MB database, 2GB bandwidth, 50,000 monthly active users
    """

    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY", "")

        # Initialize Supabase client
        if self.supabase_url and self.supabase_key:
            try:
                from supabase import create_client, Client
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                self.enabled = True
                print("✓ Supabase connected - cloud memory enabled")
            except Exception as e:
                print(f"Supabase unavailable: {e}")
                self.client = None
                self.enabled = False
        else:
            print("Supabase not configured - using local memory only")
            self.client = None
            self.enabled = False

    def create_tables(self):
        """
        SQL to create tables in Supabase (run this once):

        -- User profiles
        CREATE TABLE user_profiles (
            user_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT NOW(),
            profile_data JSONB NOT NULL,
            last_updated TIMESTAMP DEFAULT NOW()
        );

        -- Memory entries
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

        -- Session summaries
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

        -- Progress tracking
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
        """
        pass

    async def save_memory(self, entry: MemoryEntry) -> bool:
        """Save memory entry to Supabase"""
        if not self.enabled:
            return False

        try:
            data = {
                "user_id": entry.user_id,
                "session_id": entry.session_id,
                "timestamp": entry.timestamp,
                "message": entry.message,
                "emotion": entry.emotion,
                "emotion_intensity": entry.emotion_intensity,
                "therapy_mode": entry.therapy_mode,
                "entry_data": {
                    "detected_patterns": entry.detected_patterns,
                    "breakthroughs": entry.breakthroughs,
                    "concerns": entry.concerns
                }
            }

            result = self.client.table("memory_entries").insert(data).execute()
            return True

        except Exception as e:
            print(f"Error saving to Supabase: {e}")
            return False

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Retrieve user profile from Supabase"""
        if not self.enabled:
            return None

        try:
            result = self.client.table("user_profiles").select("*").eq("user_id", user_id).execute()

            if result.data and len(result.data) > 0:
                profile_data = result.data[0]["profile_data"]
                return UserProfile(**profile_data)

            return None

        except Exception as e:
            print(f"Error fetching profile: {e}")
            return None

    async def update_user_profile(self, profile: UserProfile) -> bool:
        """Update user profile in Supabase"""
        if not self.enabled:
            return False

        try:
            data = {
                "user_id": profile.user_id,
                "profile_data": asdict(profile),
                "last_updated": datetime.now().isoformat()
            }

            result = self.client.table("user_profiles").upsert(data).execute()
            return True

        except Exception as e:
            print(f"Error updating profile: {e}")
            return False

    async def get_recent_memories(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[MemoryEntry]:
        """Get recent memories for context"""
        if not self.enabled:
            return []

        try:
            result = self.client.table("memory_entries")\
                .select("*")\
                .eq("user_id", user_id)\
                .order("timestamp", desc=True)\
                .limit(limit)\
                .execute()

            memories = []
            for row in result.data:
                entry_data = row.get("entry_data", {})
                memory = MemoryEntry(
                    timestamp=row["timestamp"],
                    session_id=row["session_id"],
                    user_id=row["user_id"],
                    message=row.get("message", ""),
                    emotion=row.get("emotion", "neutral"),
                    emotion_intensity=row.get("emotion_intensity", 0.5),
                    therapy_mode=row.get("therapy_mode", "supportive"),
                    detected_patterns=entry_data.get("detected_patterns", []),
                    breakthroughs=entry_data.get("breakthroughs", []),
                    concerns=entry_data.get("concerns", [])
                )
                memories.append(memory)

            return memories

        except Exception as e:
            print(f"Error fetching memories: {e}")
            return []


class LongTermMemorySystem:
    """
    Intelligent long-term memory system
    Works with or without Supabase (graceful fallback to local)
    """

    def __init__(self):
        self.supabase_store = SupabaseMemoryStore()
        self.local_cache = {}  # In-memory cache
        self.local_storage_path = "data/memory_cache.json"
        self._load_local_cache()

    def _load_local_cache(self):
        """Load local cache from disk"""
        try:
            if os.path.exists(self.local_storage_path):
                with open(self.local_storage_path, 'r') as f:
                    self.local_cache = json.load(f)
        except Exception as e:
            print(f"Could not load local cache: {e}")
            self.local_cache = {}

    def _save_local_cache(self):
        """Save local cache to disk"""
        try:
            os.makedirs(os.path.dirname(self.local_storage_path), exist_ok=True)
            with open(self.local_storage_path, 'w') as f:
                json.dump(self.local_cache, f, indent=2)
        except Exception as e:
            print(f"Could not save local cache: {e}")

    def get_anonymous_user_id(self, session_id: str) -> str:
        """Generate anonymous but consistent user ID"""
        # Hash session ID to create consistent anonymous user ID
        return hashlib.md5(session_id.encode()).hexdigest()[:16]

    async def remember(
        self,
        user_id: str,
        session_id: str,
        message: str,
        emotion: str,
        emotion_intensity: float,
        therapy_mode: str,
        detected_patterns: List[str] = None,
        breakthroughs: List[str] = None,
        concerns: List[str] = None
    ):
        """Save memory entry"""

        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            user_id=user_id,
            message=message,
            emotion=emotion,
            emotion_intensity=emotion_intensity,
            therapy_mode=therapy_mode,
            detected_patterns=detected_patterns or [],
            breakthroughs=breakthroughs or [],
            concerns=concerns or []
        )

        # Try Supabase first
        saved_to_cloud = await self.supabase_store.save_memory(entry)

        # Always save to local cache as backup
        if user_id not in self.local_cache:
            self.local_cache[user_id] = {"memories": []}

        self.local_cache[user_id]["memories"].append(asdict(entry))

        # Keep only last 100 memories per user in local cache
        self.local_cache[user_id]["memories"] = \
            self.local_cache[user_id]["memories"][-100:]

        self._save_local_cache()

        return saved_to_cloud

    async def recall(
        self,
        user_id: str,
        context: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant memories for context"""

        # Try cloud first
        cloud_memories = await self.supabase_store.get_recent_memories(user_id, limit)

        if cloud_memories:
            return [asdict(m) for m in cloud_memories]

        # Fallback to local cache
        if user_id in self.local_cache:
            memories = self.local_cache[user_id]["memories"]
            return memories[-limit:]

        return []

    async def get_session_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's therapeutic journey"""

        memories = await self.recall(user_id, limit=50)

        if not memories:
            return {
                "new_user": True,
                "message": "Welcome! I'm here to support you."
            }

        # Analyze patterns
        emotions = [m["emotion"] for m in memories]
        emotion_counts = {}
        for e in emotions:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1

        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]

        # Calculate trend
        recent_intensities = [m["emotion_intensity"] for m in memories[-10:]]
        older_intensities = [m["emotion_intensity"] for m in memories[:10]]

        recent_avg = sum(recent_intensities) / len(recent_intensities) if recent_intensities else 0.5
        older_avg = sum(older_intensities) / len(older_intensities) if older_intensities else 0.5

        trend = "improving" if recent_avg < older_avg else "similar" if abs(recent_avg - older_avg) < 0.1 else "struggling"

        return {
            "new_user": False,
            "total_interactions": len(memories),
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotion_counts,
            "mood_trend": trend,
            "recent_avg_intensity": recent_avg,
            "last_session": memories[-1]["timestamp"] if memories else None,
            "continuity_prompt": self._generate_continuity_prompt(memories)
        }

    def _generate_continuity_prompt(self, memories: List[Dict]) -> str:
        """Generate personalized greeting based on history"""

        if not memories:
            return "Hello! I'm here to support you. How are you feeling today?"

        last_memory = memories[-1]
        last_emotion = last_memory["emotion"]

        # Check time since last session
        try:
            last_time = datetime.fromisoformat(last_memory["timestamp"])
            hours_ago = (datetime.now() - last_time).total_seconds() / 3600

            if hours_ago < 1:
                time_ref = "a little while ago"
            elif hours_ago < 24:
                time_ref = f"{int(hours_ago)} hours ago"
            else:
                days = int(hours_ago / 24)
                time_ref = f"{days} day{'s' if days > 1 else ''} ago"
        except:
            time_ref = "last time"

        prompts = {
            "sad": f"I remember {time_ref} you were feeling down. How are things now?",
            "anxious": f"We talked about your anxiety {time_ref}. Have things shifted?",
            "lonely": f"Last time you shared feeling lonely. How's your heart today?",
            "angry": f"You were processing some anger {time_ref}. Where are you with that now?",
            "happy": f"It's good to see you again! You seemed more positive {time_ref}. How are you feeling today?",
        }

        return prompts.get(last_emotion, f"Welcome back. How have you been since we last talked {time_ref}?")

    async def track_breakthrough(self, user_id: str, breakthrough: str):
        """Record a therapeutic breakthrough"""
        if user_id not in self.local_cache:
            self.local_cache[user_id] = {"breakthroughs": []}

        if "breakthroughs" not in self.local_cache[user_id]:
            self.local_cache[user_id]["breakthroughs"] = []

        self.local_cache[user_id]["breakthroughs"].append({
            "breakthrough": breakthrough,
            "timestamp": datetime.now().isoformat()
        })

        self._save_local_cache()

    async def track_concern(self, user_id: str, concern: str):
        """Record ongoing concern to revisit"""
        if user_id not in self.local_cache:
            self.local_cache[user_id] = {"concerns": []}

        if "concerns" not in self.local_cache[user_id]:
            self.local_cache[user_id]["concerns"] = []

        self.local_cache[user_id]["concerns"].append({
            "concern": concern,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        })

        self._save_local_cache()


# Testing
if __name__ == "__main__":
    import asyncio

    async def test_memory():
        memory = LongTermMemorySystem()

        user_id = memory.get_anonymous_user_id("test-session-123")

        # Save some memories
        await memory.remember(
            user_id=user_id,
            session_id="session-1",
            message="I feel so anxious",
            emotion="anxious",
            emotion_intensity=0.8,
            therapy_mode="cbt",
            detected_patterns=["catastrophizing"],
            concerns=["work stress"]
        )

        await memory.remember(
            user_id=user_id,
            session_id="session-1",
            message="I'm feeling a bit better",
            emotion="anxious",
            emotion_intensity=0.5,
            therapy_mode="cbt",
            detected_patterns=[],
            breakthroughs=["recognized thought pattern"]
        )

        # Recall memories
        memories = await memory.recall(user_id)
        print(f"✓ Saved {len(memories)} memories")

        # Get summary
        summary = await memory.get_session_summary(user_id)
        print(f"✓ Session summary generated")
        print(f"  Dominant emotion: {summary['dominant_emotion']}")
        print(f"  Mood trend: {summary['mood_trend']}")
        print(f"  Continuity prompt: {summary['continuity_prompt']}")

    asyncio.run(test_memory())
