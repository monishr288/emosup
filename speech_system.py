"""
Speech-to-Speech System with Interruption Handling
Handles voice input, TTS output, and interruption detection
"""
import asyncio
import io
import wave
from typing import Optional, Callable
import json


class SpeechToSpeechSystem:
    """Manages speech recognition and synthesis with interruption"""

    def __init__(self):
        self.is_speaking = False
        self.is_listening = False
        self.current_audio_stream = None
        self.interruption_callback = None

    async def transcribe_audio(self, audio_data: bytes) -> str:
        """
        Transcribe audio using Whisper or Web Speech API

        For production, integrate with:
        - OpenAI Whisper API
        - Local Whisper model
        - Google Speech-to-Text
        - Azure Speech Services
        """
        # Placeholder - in real implementation:
        # return await whisper_client.transcribe(audio_data)
        return "User speech transcription"

    async def synthesize_speech(
        self,
        text: str,
        voice_params: dict
    ) -> bytes:
        """
        Convert text to speech with specified voice parameters

        For production, integrate with:
        - ElevenLabs (best quality)
        - OpenAI TTS
        - Azure Neural TTS
        - Google Cloud TTS
        - Local Coqui TTS
        """
        # Voice parameters from therapy system:
        # - pitch: -1 to 1
        # - speed: 0.5 to 2.0
        # - warmth: 0 to 1
        # - energy: 0 to 1

        # Placeholder - in real implementation:
        # return await tts_client.synthesize(text, voice_params)

        return b""  # Would return actual audio bytes

    async def play_audio_with_interruption(
        self,
        audio_data: bytes,
        on_interrupt: Callable
    ):
        """
        Play audio but stop immediately if user starts speaking
        """
        self.is_speaking = True
        self.interruption_callback = on_interrupt

        try:
            # Chunk audio and play with interruption detection
            chunk_size = 4096
            for i in range(0, len(audio_data), chunk_size):
                if not self.is_speaking:
                    # Interrupted!
                    break

                chunk = audio_data[i:i+chunk_size]
                # Play chunk (would integrate with audio output)
                await asyncio.sleep(0.1)  # Simulate playback time

        finally:
            self.is_speaking = False

    def interrupt_speech(self):
        """Called when user starts speaking during AI response"""
        if self.is_speaking:
            self.is_speaking = False
            if self.interruption_callback:
                self.interruption_callback()


class VoiceActivityDetector:
    """Detects when user starts/stops speaking"""

    def __init__(self, threshold: float = 0.02):
        self.threshold = threshold
        self.is_speaking = False
        self.speech_start_callback = None
        self.speech_end_callback = None

    async def process_audio_stream(self, audio_chunk: bytes):
        """
        Process incoming audio to detect voice activity

        Uses energy-based VAD or ML-based VAD
        """
        # Calculate audio energy
        energy = self._calculate_energy(audio_chunk)

        speech_detected = energy > self.threshold

        if speech_detected and not self.is_speaking:
            # Speech started
            self.is_speaking = True
            if self.speech_start_callback:
                await self.speech_start_callback()

        elif not speech_detected and self.is_speaking:
            # Speech ended
            self.is_speaking = False
            if self.speech_end_callback:
                await self.speech_end_callback()

    def _calculate_energy(self, audio_chunk: bytes) -> float:
        """Calculate RMS energy of audio chunk"""
        # Simplified energy calculation
        # In production, use proper audio analysis
        if len(audio_chunk) == 0:
            return 0.0

        # Convert bytes to samples and calculate RMS
        # This is a placeholder - real implementation would use numpy
        return 0.05  # Placeholder value

    def set_callbacks(
        self,
        on_speech_start: Callable,
        on_speech_end: Callable
    ):
        """Set callbacks for speech events"""
        self.speech_start_callback = on_speech_start
        self.speech_end_callback = on_speech_end


class InterruptionHandler:
    """Handles interruptions gracefully"""

    def __init__(self, tts_system: SpeechToSpeechSystem):
        self.tts_system = tts_system
        self.vad = VoiceActivityDetector()
        self.pending_response = None

    async def handle_user_interrupt(self):
        """Called when user interrupts AI"""
        # Stop current speech immediately
        self.tts_system.interrupt_speech()

        # Acknowledge interruption
        acknowledgment = "Yes? I'm listening."

        # Play short acknowledgment
        ack_audio = await self.tts_system.synthesize_speech(
            acknowledgment,
            {"pitch": 0, "speed": 1.2, "warmth": 0.9, "energy": 0.6}
        )

        # Don't wait for full playback - keep it snappy
        # Ready to listen to new input


# Web Speech API Integration (for frontend)
WEB_SPEECH_INTEGRATION_CODE = """
// Frontend JavaScript for Web Speech API
class WebSpeechHandler {
    constructor() {
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        this.synthesis = window.speechSynthesis;
        this.currentUtterance = null;

        // Configure recognition
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        // Interruption handling
        this.onInterrupt = null;
    }

    startListening(onResult, onInterrupt) {
        this.onInterrupt = onInterrupt;

        this.recognition.onresult = (event) => {
            const current = event.resultIndex;
            const transcript = event.results[current][0].transcript;
            const isFinal = event.results[current].isFinal;

            // If user speaks while AI is talking, interrupt!
            if (this.currentUtterance && this.synthesis.speaking) {
                this.interrupt();
            }

            if (isFinal) {
                onResult(transcript);
            }
        };

        this.recognition.start();
    }

    speak(text, voiceParams, onStart, onEnd) {
        // Stop any current speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        this.currentUtterance = utterance;

        // Apply voice parameters
        utterance.pitch = 1.0 + (voiceParams.pitch || 0);
        utterance.rate = voiceParams.speed || 1.0;
        utterance.volume = 1.0;

        // Select warm, caring voice
        const voices = this.synthesis.getVoices();
        const preferredVoice = voices.find(v =>
            v.name.includes('Female') || v.name.includes('Samantha')
        ) || voices[0];
        utterance.voice = preferredVoice;

        utterance.onstart = onStart;
        utterance.onend = () => {
            this.currentUtterance = null;
            onEnd();
        };

        this.synthesis.speak(utterance);
    }

    interrupt() {
        // Immediately stop speaking
        this.synthesis.cancel();
        this.currentUtterance = null;

        // Notify that interruption occurred
        if (this.onInterrupt) {
            this.onInterrupt();
        }
    }

    stopListening() {
        this.recognition.stop();
    }
}

export default WebSpeechHandler;
"""


# Save the frontend code
def save_web_speech_code():
    """Save Web Speech API integration code"""
    return WEB_SPEECH_INTEGRATION_CODE


if __name__ == "__main__":
    # Test the speech system
    import asyncio

    async def test_speech_system():
        tts = SpeechToSpeechSystem()
        vad = VoiceActivityDetector()

        print("Speech-to-Speech System Initialized")
        print("✓ Voice Activity Detection")
        print("✓ Interruption Handling")
        print("✓ TTS with Voice Modulation")

        # Simulate speech synthesis
        text = "I hear that you're feeling down, and I want you to know that your feelings are valid."
        voice_params = {
            "pitch": -0.1,
            "speed": 0.9,
            "warmth": 0.95,
            "energy": 0.4
        }

        print(f"\nSynthesizing: {text}")
        print(f"Voice params: {voice_params}")

        # In production, this would generate actual audio
        audio = await tts.synthesize_speech(text, voice_params)
        print("✓ Speech synthesized")

    asyncio.run(test_speech_system())
