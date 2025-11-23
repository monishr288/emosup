'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { TextShimmer } from '@/components/ui/text-shimmer'
import { Send, X, Bot, User } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { API_BASE_URL } from '@/lib/config'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

interface ChatbotInterfaceProps {
  onClose: () => void
  initialMessage?: string
}

interface ConnectionStatus {
  status: 'checking' | 'connected' | 'disconnected' | 'error'
  message: string
  details?: any
}

export function ChatbotInterface({ onClose, initialMessage }: ChatbotInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>({
    status: 'checking',
    message: ''
  })
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load persisted messages (local session)
  useEffect(() => {
    try {
      const raw = localStorage.getItem('chat_messages')
      if (raw) {
        const parsed: Message[] = JSON.parse(raw)
        // revive timestamps
        setMessages(parsed.map(m => ({ ...m, timestamp: new Date(m.timestamp) })))
        return
      }
    } catch {}
    // If no messages, seed greeting
    setMessages([
      {
        id: '1',
        text: "Hello! I'm your emotional support companion. I'm here to listen and help. How are you feeling today?",
        sender: 'bot',
        timestamp: new Date()
      }
    ])
  }, [])

  // Persist messages
  useEffect(() => {
    try {
      localStorage.setItem('chat_messages', JSON.stringify(messages))
    } catch {}
  }, [messages])

  const checkConnection = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/flight-check`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        if (data.overall_status === 'ready') {
          setConnectionStatus({
            status: 'connected',
            message: 'All systems operational',
            details: data
          })
        } else {
          setConnectionStatus({
            status: 'disconnected',
            message: data.message || 'Some services are not ready',
            details: data
          })
        }
      } else {
        setConnectionStatus({
          status: 'error',
          message: 'Cannot connect to API server',
          details: null
        })
      }
    } catch (error) {
      setConnectionStatus({
        status: 'error',
        message: 'API server is not running. Please start the Flask server.',
        details: null
      })
    }
  }

  // Flight check on mount (silent)
  useEffect(() => {
    checkConnection()
    const interval = setInterval(checkConnection, 30000)
    return () => clearInterval(interval)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // If initialMessage provided, auto-send once on open
  useEffect(() => {
    if (!initialMessage) return
    setInput(initialMessage)
    // defer to next tick to ensure state set
    const t = setTimeout(() => {
      void sendMessage()
    }, 0)
    return () => clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialMessage])

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: input.trim(),
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.text,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data = await response.json()

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.response || "I'm here for you. Can you tell me more?",
        sender: 'bot',
        timestamp: new Date()
      }

      // Optionally append coping suggestion as a separate bot message
      const suggestion = typeof data.coping_suggestion === 'string' ? data.coping_suggestion.trim() : ''
      if (suggestion && (data.emotion && !['happy', 'neutral'].includes(String(data.emotion)))) {
        const tip: Message = {
          id: (Date.now() + 2).toString(),
          text: `Tip: ${suggestion}`,
          sender: 'bot',
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botMessage, tip])
      } else {
        setMessages(prev => [...prev, botMessage])
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `I'm having trouble connecting to the server. Please make sure the Flask API server is running:\n\n1. Open a terminal in this folder\n2. Run: python api_server.py\n3. Wait for 'Running on http://0.0.0.0:5000'\n4. Then try sending your message again\n\nAPI base: ${API_BASE_URL}`,
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0c0414] via-purple-900 to-[#0c0414] text-white">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-[#1c1528]/80 backdrop-blur-sm border-b border-purple-500/20">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-400 to-blue-500 rounded-full flex items-center justify-center">
                <Bot className="w-6 h-6" />
              </div>
              <div>
                <h2 className="font-bold text-lg">EmoSupport</h2>
                <p className="text-xs text-gray-400">Your emotional support companion</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="text-white hover:bg-purple-500/20"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>
          {/* Connection status visuals removed per request */}
        </div>
      </div>

      {/* Messages */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        <div className="space-y-4 pb-24">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex gap-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.sender === 'bot' && (
                  <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                )}
                <Card
                  className={`max-w-[80%] ${
                    message.sender === 'user'
                      ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white border-0'
                      : 'bg-[#1c1528] border-purple-500/20 text-white'
                  }`}
                >
                  <div className="p-4">
                    <p className="text-sm leading-relaxed whitespace-pre-wrap">
                      {message.text}
                    </p>
                  </div>
                </Card>
                {message.sender === 'user' && (
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-white" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex gap-3 justify-start"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-blue-500 rounded-full flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <Card className="bg-[#1c1528] border-purple-500/20">
                <div className="p-4">
                  <TextShimmer className="text-sm" duration={1}>
                    Thinking...
                  </TextShimmer>
                </div>
              </Card>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-[#1c1528]/80 backdrop-blur-sm border-t border-purple-500/20">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Share what's on your mind..."
              className="flex-1 bg-[#0c0414] border-purple-500/20 text-white placeholder:text-gray-500 focus:border-purple-500"
              disabled={isLoading}
            />
            <Button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white border-0"
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
