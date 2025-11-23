'use client'

import { useState } from 'react'
import { Hero1 } from '@/components/ui/hero-1'
import { ChatbotInterface } from '@/components/chatbot-interface'

export default function Home() {
  const [showChatbot, setShowChatbot] = useState(false)
  const [initialMessage, setInitialMessage] = useState<string | undefined>()

  return (
    <div className="relative">
      {!showChatbot ? (
        <div>
          <Hero1 
            onStartChat={() => { setInitialMessage(undefined); setShowChatbot(true) }}
            onQuickPrompt={(text) => { setInitialMessage(text); setShowChatbot(true) }}
          />
        </div>
      ) : (
        <ChatbotInterface 
          initialMessage={initialMessage}
          onClose={() => setShowChatbot(false)} 
        />
      )}
    </div>
  )
}

