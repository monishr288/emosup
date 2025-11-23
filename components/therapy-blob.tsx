'use client'

import { useEffect, useRef, useState } from 'react'
import { motion, useAnimation } from 'framer-motion'

interface TherapyBlobProps {
  isListening: boolean
  isSpeaking: boolean
  isThinking: boolean
  audioLevel: number // 0-1 for visualization
  emotion?: string
}

export function TherapyBlob({
  isListening,
  isSpeaking,
  isThinking,
  audioLevel = 0,
  emotion = 'neutral'
}: TherapyBlobProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const animationFrameRef = useRef<number>()
  const controls = useAnimation()

  // Blob color based on state
  const getBlobColor = () => {
    if (isListening) return { primary: '#4ECDC4', secondary: '#44A08D' } // Teal
    if (isSpeaking) return { primary: '#667eea', secondary: '#764ba2' } // Purple
    if (isThinking) return { primary: '#f093fb', secondary: '#f5576c' } // Pink
    return { primary: '#6B7FD7', secondary: '#4E65D8' } // Calm blue
  }

  // Animated blob using canvas
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height
    const centerX = width / 2
    const centerY = height / 2

    let phase = 0
    let pulsePhase = 0

    const drawBlob = () => {
      ctx.clearRect(0, 0, width, height)

      const colors = getBlobColor()

      // Create gradient
      const gradient = ctx.createRadialGradient(
        centerX, centerY, 0,
        centerX, centerY, 200
      )
      gradient.addColorStop(0, colors.primary)
      gradient.addColorStop(1, colors.secondary)

      // Calculate blob shape with organic movement
      const points = 12
      const baseRadius = 120

      ctx.beginPath()

      for (let i = 0; i <= points; i++) {
        const angle = (i / points) * Math.PI * 2

        // Organic wobble
        const wobble = Math.sin(phase + i) * 15

        // Audio reactivity
        const audioReact = isListening || isSpeaking ? audioLevel * 30 : 0

        // Breathing animation
        const breathe = Math.sin(pulsePhase) * 10

        // Thinking pulse
        const thinkingPulse = isThinking ? Math.sin(pulsePhase * 3) * 8 : 0

        const radius = baseRadius + wobble + audioReact + breathe + thinkingPulse

        const x = centerX + Math.cos(angle) * radius
        const y = centerY + Math.sin(angle) * radius

        if (i === 0) {
          ctx.moveTo(x, y)
        } else {
          // Smooth curves
          const prevAngle = ((i - 1) / points) * Math.PI * 2
          const prevRadius = baseRadius + Math.sin(phase + (i - 1)) * 15 + audioReact + breathe + thinkingPulse
          const prevX = centerX + Math.cos(prevAngle) * prevRadius
          const prevY = centerY + Math.sin(prevAngle) * prevRadius

          const cpX = (prevX + x) / 2
          const cpY = (prevY + y) / 2

          ctx.quadraticCurveTo(prevX, prevY, cpX, cpY)
        }
      }

      ctx.closePath()
      ctx.fillStyle = gradient
      ctx.fill()

      // Glow effect when speaking
      if (isSpeaking) {
        ctx.shadowBlur = 40
        ctx.shadowColor = colors.primary
        ctx.fill()
      }

      // Inner pulse for listening
      if (isListening) {
        const pulseRadius = 80 + Math.sin(pulsePhase * 2) * 20
        ctx.beginPath()
        ctx.arc(centerX, centerY, pulseRadius, 0, Math.PI * 2)
        ctx.fillStyle = `${colors.primary}40` // Semi-transparent
        ctx.fill()
      }

      // Update phases
      phase += 0.02
      pulsePhase += 0.05

      animationFrameRef.current = requestAnimationFrame(drawBlob)
    }

    drawBlob()

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [isListening, isSpeaking, isThinking, audioLevel])

  // Face expression overlay
  const renderFace = () => {
    if (isListening) {
      return (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-white text-6xl">👂</div>
        </div>
      )
    }

    if (isSpeaking) {
      return (
        <div className="absolute inset-0 flex items-center justify-center">
          {/* Animated talking mouth */}
          <motion.div
            className="flex flex-col items-center gap-4"
            animate={{
              scale: [1, 1.05, 1],
            }}
            transition={{
              duration: 0.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            {/* Eyes */}
            <div className="flex gap-8">
              <motion.div
                className="w-4 h-4 bg-white rounded-full"
                animate={{
                  scaleY: [1, 0.3, 1]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  repeatDelay: 2
                }}
              />
              <motion.div
                className="w-4 h-4 bg-white rounded-full"
                animate={{
                  scaleY: [1, 0.3, 1]
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  repeatDelay: 2
                }}
              />
            </div>
            {/* Talking mouth */}
            <motion.div
              className="w-12 h-6 bg-white rounded-full"
              animate={{
                scaleY: [1, 1.3, 0.8, 1.2, 1],
              }}
              transition={{
                duration: 0.6,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
          </motion.div>
        </div>
      )
    }

    if (isThinking) {
      return (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="flex flex-col items-center gap-4">
            {/* Eyes looking up */}
            <div className="flex gap-8">
              <div className="w-4 h-4 bg-white rounded-full relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-800 rounded-full" />
              </div>
              <div className="w-4 h-4 bg-white rounded-full relative">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 bg-gray-800 rounded-full" />
              </div>
            </div>
            {/* Thinking dots */}
            <div className="flex gap-2">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-2 h-2 bg-white rounded-full"
                  animate={{
                    y: [0, -10, 0],
                    opacity: [0.5, 1, 0.5]
                  }}
                  transition={{
                    duration: 0.6,
                    repeat: Infinity,
                    delay: i * 0.2
                  }}
                />
              ))}
            </div>
          </div>
        </div>
      )
    }

    // Neutral/calm face
    return (
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          {/* Calm eyes */}
          <div className="flex gap-8">
            <div className="w-4 h-4 bg-white rounded-full" />
            <div className="w-4 h-4 bg-white rounded-full" />
          </div>
          {/* Gentle smile */}
          <div className="w-12 h-2 bg-white rounded-full" />
        </div>
      </div>
    )
  }

  return (
    <div className="relative w-[400px] h-[400px]">
      <canvas
        ref={canvasRef}
        width={400}
        height={400}
        className="absolute inset-0"
      />
      {renderFace()}

      {/* Status text */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2">
        <motion.p
          className="text-white text-sm font-medium px-4 py-2 rounded-full bg-black/30 backdrop-blur-sm"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          key={isListening ? 'listening' : isSpeaking ? 'speaking' : isThinking ? 'thinking' : 'ready'}
        >
          {isListening ? '🎤 Listening to you...' :
           isSpeaking ? '💬 Speaking...' :
           isThinking ? '🤔 Thinking...' :
           '😌 I\'m here for you'}
        </motion.p>
      </div>
    </div>
  )
}
