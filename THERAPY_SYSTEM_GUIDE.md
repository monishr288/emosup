# Advanced Voice Therapy System 🧠💜

## What's New

Your emotional support chatbot now has **professional-grade therapy capabilities** with voice interaction and an animated therapy companion!

## Features

### 🎭 Multi-Agent Therapy System

**5 Specialized AI Agents working together:**

1. **Therapist Agent** - Main therapeutic conversation with CBT/DBT techniques
2. **Emotion Analyzer** - Deep emotion detection and intensity analysis
3. **Memory Agent** - Tracks patterns, progress, and therapeutic alliance
4. **Crisis Agent** - Immediate crisis detection and intervention
5. **CBT/DBT Agent** - Cognitive behavioral therapy and dialectical techniques

### 🎯 Therapeutic Capabilities

**Evidence-Based Approaches:**
- **CBT (Cognitive Behavioral Therapy)** - Challenges negative thought patterns
- **DBT (Dialectical Behavior Therapy)** - Emotion regulation skills
- **Motivational Interviewing** - Builds motivation for change
- **Solution-Focused Therapy** - Focuses on solutions, not just problems
- **Supportive Therapy** - Pure empathy and validation

**What It Can Do:**
- ✅ Detect cognitive distortions (all-or-nothing thinking, catastrophizing, etc.)
- ✅ Provide Socratic questioning to explore thoughts
- ✅ Offer evidence-based coping techniques
- ✅ Validate emotions while gently challenging unhelpful thoughts
- ✅ Track emotional patterns over time
- ✅ Adapt therapy mode based on your emotional state
- ✅ Provide behavioral activation suggestions
- ✅ Teach mindfulness and grounding techniques

### 🎙️ Speech-to-Speech Interaction

**Voice Features:**
- **Real-time speech recognition** - Speak naturally, it understands you
- **Intelligent interruption handling** - Start talking and it stops immediately
- **Emotion-aware voice synthesis** - Voice tone adapts to your emotion
- **Voice parameters**:
  - Pitch adjustment (lower for calming, higher for energy)
  - Speed modulation (slower for distress, normal for engagement)
  - Warmth level (always high, extra warm for difficult emotions)
  - Energy level (calm for anxiety, gentle for sadness)

**How It Works:**
1. Click "Start Talking" to begin
2. Speak your thoughts and feelings
3. The blob listens and shows live audio visualization
4. When you finish, it thinks and responds with appropriate voice tone
5. **Interrupt anytime** by just speaking - it stops immediately

### 🎨 Animated Therapy Blob

**Visual States:**
- 🟢 **Listening** - Teal color, pulsing with your voice level
- 🟣 **Speaking** - Purple color, animated talking mouth
- 🔴 **Thinking** - Pink color, thoughtful expression with dots
- 🔵 **Neutral** - Calm blue, gentle breathing animation

**Facial Expressions:**
- Listening: Ear emoji + active pulse
- Speaking: Animated eyes and moving mouth
- Thinking: Eyes looking up + thought dots
- Calm: Gentle smile

**Organic Animations:**
- Breathing motion (always active)
- Audio-reactive wobbling
- Smooth morphing between states
- Glow effects during speech
- Natural blob physics

## How to Use

### Quick Start

1. **Start the API Server** (if not running):
   ```bash
   python3 api_server.py
   ```

2. **Start Next.js Frontend**:
   ```bash
   npm run dev
   ```

3. **Navigate to Therapy Interface**:
   ```
   http://localhost:3000/therapy
   ```

4. **Allow Microphone Access** when prompted

5. **Click "Start Talking"** and begin your therapy session!

### Using Voice Therapy

**Best Practices:**
- Speak naturally, like talking to a friend
- You can interrupt at any time - just start speaking
- The blob shows when it's listening (teal) vs speaking (purple)
- Take your time - there's no rush
- Be honest about your feelings

**Controls:**
- 🎤 **Green Button**: Start/stop listening
- 🔊 **Sound Icon**: Enable/disable voice responses
- 🔄 **Reset Icon**: Start a new therapy session

### Understanding Therapy Modes

The AI automatically chooses the best approach based on your emotion:

**High Intensity (>0.8)** → **Supportive Mode**
- Pure validation and empathy
- No challenging, just presence
- Example: "What you're feeling makes complete sense..."

**Anxiety/Stress** → **CBT Mode**
- Identifies thought patterns
- Gentle challenging
- Evidence-based questioning
- Example: "What evidence do you have for this thought?"

**Anger/Frustration** → **DBT Mode**
- Emotion regulation
- Acceptance techniques
- Opposite action skills
- Example: "Let's work on accepting these intense emotions..."

**Low Motivation** → **Motivational Interviewing**
- Values exploration
- Building intrinsic motivation
- Example: "What matters most to you right now?"

**Solution-Needed** → **Solution-Focused**
- Past successes
- Actionable steps
- Example: "When was a time you handled something similar?"

## Therapeutic Techniques

### Cognitive Distortions Detection

The system automatically detects:
- **All-or-Nothing Thinking** - "I always fail"
- **Overgeneralization** - "This never works"
- **Catastrophizing** - "It's a complete disaster"
- **Should Statements** - "I should have done better"
- **Emotional Reasoning** - "I feel worthless, so I must be"

### Coping Techniques Suggested

**For Anxiety:**
- Box breathing (4-4-4-4)
- Progressive muscle relaxation
- 5-4-3-2-1 grounding
- Worry time technique

**For Sadness:**
- Behavioral activation
- Gratitude journaling
- Social connection
- Self-compassion

**For Anger:**
- STOP skill (DBT)
- Opposite action
- Physical release
- Time-out strategy

**For Loneliness:**
- Schedule social activity
- Join communities
- Volunteering
- Self-companionship

## Technical Architecture

### Backend (Python)

```
therapy_agent_system.py (343 lines)
├── TherapySystem (Orchestrator)
├── TherapistAgent (Main therapist)
│   ├── Cognitive distortion detection
│   ├── Therapy mode selection
│   ├── Response generation
│   └── Voice tone determination
├── MemoryAgent (Long-term tracking)
│   ├── Emotion pattern tracking
│   ├── Progress notes
│   └── User profile
└── CrisisAgent (Safety)
    └── Crisis keyword detection
```

### Frontend (React/TypeScript)

```
components/voice-therapy-interface.tsx
├── Web Speech API Integration
├── Voice Activity Detection
├── Interruption Handling
└── Message History

components/therapy-blob.tsx
├── Canvas-based Animation
├── State-reactive Morphing
├── Facial Expression System
└── Audio Visualization
```

### API Endpoints

**POST `/api/therapy`**
```json
Request:
{
  "message": "I feel so overwhelmed"
}

Response:
{
  "response": "Therapeutic response...",
  "emotion": "anxious",
  "therapy_mode": "cbt",
  "session_phase": "exploration",
  "is_crisis": false,
  "voice_tone": {
    "pitch": -0.1,
    "speed": 0.9,
    "warmth": 0.95,
    "energy": 0.4
  },
  "suggested_techniques": ["Box breathing", "Grounding"],
  "detected_distortions": ["catastrophizing"]
}
```

## Example Therapy Session

**User**: "I always mess everything up. I'm such a failure."

**System Detects:**
- Emotion: sad (intensity: 0.8)
- Distortion: all-or-nothing thinking, overgeneralization
- Mode: CBT

**Therapist Response**:
> "What you're feeling makes complete sense given what you're experiencing. Your emotions are valid and deserve to be acknowledged.
>
> It sounds like you're carrying a lot of sadness right now.
>
> I notice you might be seeing things in black and white. Are there any exceptions? Has there been a time when this wasn't true?
>
> What evidence do you have for this thought?"

**Voice Tone:**
- Pitch: -0.1 (lower, calming)
- Speed: 0.85 (slower, more gentle)
- Warmth: 0.95 (very warm)
- Energy: 0.3 (calm, measured)

## Customization

### Adjust Voice Parameters

Edit `therapy_agent_system.py`, method `_determine_voice_tone()`:

```python
# Make voice even warmer
base_tone["warmth"] = 1.0

# Speak slower for all emotions
base_tone["speed"] = 0.8
```

### Add New Therapy Techniques

Edit `therapy_agent_system.py`, `cbt_techniques` dictionary:

```python
self.cbt_techniques = {
    "thought_challenging": [
        "Your new technique here",
        # ...existing techniques
    ]
}
```

### Change Blob Appearance

Edit `components/therapy-blob.tsx`:

```typescript
// Base size
const baseRadius = 150  // Make smaller

// Animation speed
phase += 0.01  // Slower movement

// Colors
const colors = { primary: '#YOUR_COLOR', secondary: '#YOUR_COLOR' }
```

## Browser Compatibility

**Web Speech API Support:**
- ✅ Chrome/Edge (Recommended)
- ✅ Safari
- ⚠️  Firefox (Limited support)

**For Best Experience:**
- Use Chrome or Edge
- Allow microphone permissions
- Use headphones to prevent echo
- Quiet environment for better recognition

## Privacy & Safety

**Privacy:**
- All speech processing happens in your browser (Web Speech API)
- No audio is recorded or saved
- Conversations stored locally only
- No data sent to external servers (except therapy API)

**Safety:**
- Crisis detection is automatic
- Emergency resources provided immediately
- Session can be reset anytime
- Not a replacement for professional therapy

**Disclaimers:**
⚠️ This is an AI therapy companion, NOT a licensed therapist
⚠️ In crisis, call 988 (US) or local emergency services
⚠️ Use alongside, not instead of, professional mental health care

## Troubleshooting

### Microphone Not Working
- Check browser permissions (🔒 icon in address bar)
- Make sure microphone is not used by another app
- Try reloading the page

### Voice Recognition Issues
- Speak clearly and at normal volume
- Reduce background noise
- Check if language is set to English (en-US)

### Blob Not Animating
- Make sure JavaScript is enabled
- Try a different browser (Chrome recommended)
- Check browser console for errors

### API Not Responding
- Ensure Flask API is running: `python3 api_server.py`
- Check API is accessible: `http://localhost:5000/api/health`
- Restart API server if needed

## Future Enhancements

**Planned Features:**
- [ ] Session summaries and insights
- [ ] Progress tracking over time
- [ ] Personalized therapy goals
- [ ] Integration with professional therapists
- [ ] Mobile app version
- [ ] Multiple language support
- [ ] Advanced voice synthesis (ElevenLabs)
- [ ] Whisper for better speech recognition

## Credits

**Built with:**
- React + Next.js 14 (Frontend)
- Flask + Python (Backend)
- Web Speech API (Voice I/O)
- Framer Motion (Animations)
- Canvas API (Blob rendering)
- Evidence-based CBT/DBT techniques

**Inspired by:**
- Cognitive Behavioral Therapy (Aaron Beck)
- Dialectical Behavior Therapy (Marsha Linehan)
- Motivational Interviewing (Miller & Rollnick)
- Person-Centered Therapy (Carl Rogers)

---

**Remember:** This is a therapeutic tool designed to supplement, not replace, professional mental health care. If you're experiencing a mental health crisis, please reach out to:

- National Suicide Prevention Lifeline: **988** (US)
- Crisis Text Line: Text **HOME** to **741741**
- International: https://www.iasp.info/resources/Crisis_Centres/
- Emergency Services: **911** or your local emergency number

---

**You deserve support, compassion, and healing. 💜**
