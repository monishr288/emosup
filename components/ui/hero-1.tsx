"use client";

import * as React from "react";
import { type MouseEvent } from "react";

interface Hero1Props {
  onStartChat?: () => void
  onQuickPrompt?: (text: string) => void
}

const Hero1 = ({ onStartChat, onQuickPrompt }: Hero1Props) => {
  const handleInputClick = () => {
    if (onStartChat) {
      onStartChat()
    }
  }

  const handleSuggestionClick = (e: MouseEvent<HTMLButtonElement>) => {
    const text = (e.currentTarget.dataset.prompt || "").trim()
    if (!text) return
    if (onQuickPrompt) onQuickPrompt(text)
    else if (onStartChat) onStartChat()
  }

  return (
    <div className="min-h-screen bg-[#0c0414] text-white flex flex-col relative overflow-x-hidden">
      {/* Gradient */}
      <div className="flex gap-[10rem] rotate-[-20deg] absolute top-[-40rem] right-[-30rem] z-[0] blur-[4rem] skew-[-40deg]  opacity-50">
        <div className="w-[10rem] h-[20rem] bg-gradient-to-br from-white to-blue-300"></div>
        <div className="w-[10rem] h-[20rem] bg-gradient-to-br from-white to-blue-300"></div>
        <div className="w-[10rem] h-[20rem] bg-gradient-to-br from-white to-blue-300"></div>
      </div>
      <div className="flex gap-[10rem] rotate-[-20deg] absolute top-[-50rem] right-[-50rem] z-[0] blur-[4rem] skew-[-40deg]  opacity-50">
        <div className="w-[10rem] h-[20rem] bg-gradient-to-br from-white to-blue-300"></div>
        <div className="w-[10rem] h-[20rem] bg-gradient-to-br from-white to-blue-300"></div>
        <div className="w-[10rem] h-[20rem] bg-gradient-to-br from-white to-blue-300"></div>
      </div>
      <div className="flex gap-[10rem] rotate-[-20deg] absolute top-[-60rem] right-[-60rem] z-[0] blur-[4rem] skew-[-40deg]  opacity-50">
        <div className="w-[10rem] h-[30rem] bg-gradient-to-br from-white to-blue-300"></div>
        <div className="w-[10rem] h-[30rem] bg-gradient-to-br from-white to-blue-300"></div>
        <div className="w-[10rem] h-[30rem] bg-gradient-to-br from-white to-blue-300"></div>
      </div>
      {/* Header */}
      <header className="flex justify-between items-center p-6">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-400 to-blue-500 rounded-lg flex items-center justify-center text-white font-bold text-lg">
            💚
          </div>
          <div className="font-bold text-md">EmoSupport</div>
        </div>
        {/* Get Started removed as requested */}
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 text-center">
        <div className="max-w-4xl mx-auto space-y-6">
          <div className="flex-1 flex justify-center">
            <div className="bg-[#1c1528] rounded-full px-4 py-2 flex items-center gap-2  w-fit mx-4">
              <span className="text-xs flex items-center gap-2">
                <span className="bg-black p-1 rounded-full">🥳</span>
                Introducing Emotional Support Companion
              </span>
            </div>
          </div>
          {/* Headline */}
          <h1 className="text-5xl font-bold leading-tight">
            Your 24/7 Emotional Support Companion
          </h1>

          {/* Subtitle */}
          <p className="text-md">
            A compassionate AI friend ready to listen, support, and help you through your emotional journey.
          </p>

          {/* Search bar simplified (icon buttons removed) */}
          <div className="relative max-w-2xl mx-auto w-full">
            <div className="bg-[#1c1528] rounded-full p-3 flex items-center">
              <input
                type="text"
                placeholder="How are you feeling today?"
                className="bg-transparent flex-1 outline-none text-gray-300 pl-2 cursor-pointer"
                onClick={handleInputClick}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && onStartChat) {
                    onStartChat()
                  }
                }}
                readOnly
              />
            </div>
          </div>

          {/* Suggestion pills */}
          <div className="flex flex-wrap justify-center gap-2 mt-12 max-w-2xl mx-auto">
            <button 
              data-prompt="I'm feeling anxious"
              onClick={handleSuggestionClick}
              className="bg-[#1c1528] hover:bg-[#2a1f3d] rounded-full px-4 py-2 text-sm transition-all">
              Feeling anxious?
            </button>
            <button 
              data-prompt="I need someone to talk to"
              onClick={handleSuggestionClick}
              className="bg-[#1c1528] hover:bg-[#2a1f3d] rounded-full px-4 py-2 text-sm transition-all">
              Need someone to talk to?
            </button>
            <button 
              data-prompt="Can you share some coping strategies?"
              onClick={handleSuggestionClick}
              className="bg-[#1c1528] hover:bg-[#2a1f3d] rounded-full px-4 py-2 text-sm transition-all">
              Coping strategies
            </button>
            <button 
              data-prompt="I'd like to track my mood"
              onClick={handleSuggestionClick}
              className="bg-[#1c1528] hover:bg-[#2a1f3d] rounded-full px-4 py-2 text-sm transition-all">
              Mood tracking
            </button>
            <button 
              data-prompt="I need emotional support"
              onClick={handleSuggestionClick}
              className="bg-[#1c1528] hover:bg-[#2a1f3d] rounded-full px-4 py-2 text-sm transition-all">
              Emotional support
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export { Hero1 };

