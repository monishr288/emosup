'use client'

import { useState, useEffect, useRef } from 'react'
import { TherapyBlob } from './therapy-blob'
import { Button } from '@/components/ui/button'
import { Mic, MicOff, Volume2, VolumeX, RotateCcw } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { API_BASE_URL } from '@/lib/config'

interface Message {
  id: string
  text: string
  sender: 'user' | 'therapist'
  timestamp: Date
  emotion?: string
  therapyMode?: string
}

export function VoiceTherapyInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [isThinking, setIsThinking] = useState(false)
  const [audioLevel, setAudioLevel] = useState(0)
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  const [interimTranscript, setInterimTranscript] = useState('')

  const recognitionRef = useRef<any>(null)
  const synthesisRef = useRef<SpeechSynthesis | null>(null)
  const currentUtteranceRef = useRef<SpeechSynthesisUtterance | null>(null)
  const audioContextRef = useRef<AudioContext | null>(null)
  const analyserRef = useRef<AnalyserNode | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Initialize Web Speech API
  useEffect(() => {
    if (typeof window === 'undefined') return

    // Speech Recognition
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition()
      recognition.continuous = true
      recognition.interimResults = true
      recognition.lang = 'en-US'

      recognition.onresult = (event: any) => {
        let interim = ''
        let final = ''

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript
          if (event.results[i].isFinal) {
            final += transcript
          } else {
            interim += transcript
          }
        }

        setInterimTranscript(interim)

        if (final) {
          // User spoke while AI was talking - interrupt!
          if (isSpeaking) {
            interruptSpeech()
          }
          handleUserSpeech(final)
          setInterimTranscript('')
        }
      }

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error)
        setIsListening(false)
      }

      recognition.onend = () => {
        // Auto-restart if still supposed to be listening
        if (isListening) {
          recognition.start()
        }
      }

      recognitionRef.current = recognition
    }

    // Speech Synthesis
    synthesisRef.current = window.speechSynthesis

    // Audio visualization
    if (typeof AudioContext !== 'undefined') {
      audioContextRef.current = new AudioContext()
    }

    // Initial greeting
    const greeting: Message = {
      id: Date.now().toString(),
      text: "Hello, I'm your therapy companion. I'm here to listen, support you, and help you work through whatever you're experiencing. How are you feeling today?",
      sender: 'therapist',
      timestamp: new Date(),
      therapyMode: 'supportive'
    }
    setMessages([greeting])

    if (voiceEnabled) {
      setTimeout(() => {
        speak(greeting.text, { pitch: 0, speed: 1.0, warmth: 0.9, energy: 0.6 })
      }, 1000)
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
      if (synthesisRef.current) {
        synthesisRef.current.cancel()
      }
    }
  }, [])

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Audio visualization
  useEffect(() => {
    if (!isListening || !audioContextRef.current) return

    const audioContext = audioContextRef.current

    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const source = audioContext.createMediaStreamSource(stream)
        const analyser = audioContext.createAnalyser()
        analyser.fftSize = 256
        source.connect(analyser)
        analyserRef.current = analyser

        const dataArray = new Uint8Array(analyser.frequencyBinCount)

        const updateLevel = () => {
          if (!isListening) return

          analyser.getByteFrequencyData(dataArray)
          const average = dataArray.reduce((a, b) => a + b) / dataArray.length
          setAudioLevel(average / 255)

          requestAnimationFrame(updateLevel)
        }

        updateLevel()
      })
      .catch(err => console.error('Microphone access error:', err))
  }, [isListening])

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true)
      recognitionRef.current.start()
    }
  }

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      setIsListening(false)
      recognitionRef.current.stop()
    }
  }

  const speak = (text: string, voiceParams: any) => {
    if (!synthesisRef.current || !voiceEnabled) return

    // Stop any current speech
    synthesisRef.current.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    currentUtteranceRef.current = utterance

    // Apply voice parameters from therapy system
    utterance.pitch = 1.0 + (voiceParams.pitch || 0)
    utterance.rate = voiceParams.speed || 1.0
    utterance.volume = 1.0

    // Select warm, caring voice
    const voices = synthesisRef.current.getVoices()
    const femaleVoice = voices.find(v =>
      v.name.includes('Female') ||
      v.name.includes('Samantha') ||
      v.name.includes('Victoria') ||
      v.lang.includes('en')
    ) || voices[0]

    if (femaleVoice) {
      utterance.voice = femaleVoice
    }

    utterance.onstart = () => {
      setIsSpeaking(true)
      setIsThinking(false)
    }

    utterance.onend = () => {
      setIsSpeaking(false)
      currentUtteranceRef.current = null
      // Auto-start listening after therapist finishes
      if (voiceEnabled) {
        setTimeout(startListening, 500)
      }
    }

    utterance.onerror = () => {
      setIsSpeaking(false)
      currentUtteranceRef.current = null
    }

    synthesisRef.current.speak(utterance)
  }

  const interruptSpeech = () => {
    if (synthesisRef.current) {
      synthesisRef.current.cancel()
      setIsSpeaking(false)
      currentUtteranceRef.current = null
    }
  }

  const handleUserSpeech = async (transcript: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      text: transcript,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsThinking(true)
    stopListening()

    try {
      // Call therapy API
      const response = await fetch(`${API_BASE_URL}/api/therapy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: transcript })
      })

      if (!response.ok) throw new Error('Therapy API failed')

      const data = await response.json()

      const therapistMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response,
        sender: 'therapist',
        timestamp: new Date(),
        emotion: data.emotion,
        therapyMode: data.therapy_mode
      }

      setMessages(prev => [...prev, therapistMessage])
      setIsThinking(false)

      // Speak the response
      if (voiceEnabled && data.voice_tone) {
        speak(data.response, data.voice_tone)
      } else {
        setTimeout(startListening, 500)
      }

    } catch (error) {
      console.error('Error:', error)
      setIsThinking(false)

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm here with you. Could you tell me again what's on your mind?",
        sender: 'therapist',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, errorMessage])

      if (voiceEnabled) {
        speak(errorMessage.text, { pitch: 0, speed: 0.9, warmth: 1.0, energy: 0.5 })
      } else {
        setTimeout(startListening, 500)
      }
    }
  }

  const resetSession = () => {
    setMessages([])
    setIsListening(false)
    setIsSpeaking(false)
    setIsThinking(false)
    interruptSpeech()
    stopListening()

    // Re-greet
    setTimeout(() => {
      const greeting: Message = {
        id: Date.now().toString(),
        text: "Let's start fresh. I'm here to listen. What would you like to talk about?",
        sender: 'therapist',
        timestamp: new Date()
      }
      setMessages([greeting])
      if (voiceEnabled) {
        speak(greeting.text, { pitch: 0, speed: 1.0, warmth: 0.9, energy: 0.6 })
      }
    }, 500)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

          {/* Left: Animated Blob Character */}
          <div className="flex flex-col items-center justify-center">
            <TherapyBlob
              isListening={isListening}
              isSpeaking={isSpeaking}
              isThinking={isThinking}
              audioLevel={audioLevel}
            />

            {/* Controls */}
            <div className="mt-8 flex gap-4">
              <Button
                onClick={isListening ? stopListening : startListening}
                size="lg"
                className={`${
                  isListening
                    ? 'bg-red-500 hover:bg-red-600'
                    : 'bg-green-500 hover:bg-green-600'
                } text-white rounded-full px-8`}
              >
                {isListening ? (
                  <>
                    <MicOff className="mr-2" />
                    Stop Listening
                  </>
                ) : (
                  <>
                    <Mic className="mr-2" />
                    Start Talking
                  </>
                )}
              </Button>

              <Button
                onClick={() => {
                  setVoiceEnabled(!voiceEnabled)
                  if (!voiceEnabled) {
                    interruptSpeech()
                  }
                }}
                size="lg"
                variant="outline"
                className="rounded-full"
              >
                {voiceEnabled ? <Volume2 /> : <VolumeX />}
              </Button>

              <Button
                onClick={resetSession}
                size="lg"
                variant="outline"
                className="rounded-full"
              >
                <RotateCcw />
              </Button>
            </div>

            {/* Interim transcript */}
            {interimTranscript && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 px-6 py-3 bg-white/10 backdrop-blur-sm rounded-full"
              >
                <p className="text-white text-sm italic">&quot;{interimTranscript}...&quot;</p>
              </motion.div>
            )}
          </div>

          {/* Right: Conversation Transcript */}
          <div className="bg-white/5 backdrop-blur-lg rounded-3xl p-6 border border-white/10">
            <h2 className="text-2xl font-bold text-white mb-6">Therapy Session</h2>

            <div className="h-[500px] overflow-y-auto space-y-4 mb-6">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, x: message.sender === 'user' ? 20 : -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0 }}
                    className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-2xl px-5 py-3 ${
                        message.sender === 'user'
                          ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                          : 'bg-white/10 text-white border border-white/20'
                      }`}
                    >
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">
                        {message.text}
                      </p>
                      {message.therapyMode && (
                        <p className="text-xs opacity-60 mt-2">
                          Mode: {message.therapyMode}
                        </p>
                      )}
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </div>

            <div className="text-center text-white/60 text-sm">
              <p>💜 Your conversation is private and supportive</p>
              <p className="mt-2 text-xs">
                This is not a replacement for professional therapy
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
