import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const SYSTEM_PROMPT =
  "You are MindEase, a warm, supportive AI companion for emotional support. " +
  "Your goal is to reduce loneliness, listen empathetically, and respond in a calm, encouraging tone. " +
  "Avoid giving medical advice or crisis counseling. Keep replies short, kind, and easy to understand.";

const STORAGE_KEY = "mindease_chat_history_v1";
const THEME_KEY = "mindease_theme";

function Chat() {
  const [showWelcome, setShowWelcome] = useState(true);
  const [darkMode, setDarkMode] = useState(() => {
    // Check localStorage for saved theme preference
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme) {
      return savedTheme === "dark";
    }
    // Check system preference
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });
  
  const [messages, setMessages] = useState(() => {
    // load history from localStorage
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [
        {
          id: 1,
          sender: "bot",
          text: "Hi, I'm MindEase. I'm here to listen. How are you feeling right now?",
          timestamp: new Date().toLocaleTimeString(),
        },
      ];
      return JSON.parse(raw);
    } catch {
      return [
        {
          id: 1,
          sender: "bot",
          text: "Hi, I'm MindEase. I'm here to listen. How are you feeling right now?",
          timestamp: new Date().toLocaleTimeString(),
        },
      ];
    }
  });

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // attachments
  const [attachedFiles, setAttachedFiles] = useState([]);

  // audio recording
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const messagesEndRef = useRef(null);

  // Apply theme class to body
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
    localStorage.setItem(THEME_KEY, darkMode ? "dark" : "light");
  }, [darkMode]);

  // Welcome animation timer
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowWelcome(false);
    }, 3000); // 3 seconds
    return () => clearTimeout(timer);
  }, []);

  // persist history whenever messages change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
  }, [messages]);

  // scroll to end
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files || []);
    setAttachedFiles(files);
  };

  const clearAttachments = () => {
    setAttachedFiles([]);
  };

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed && attachedFiles.length === 0) return;
    if (loading) return;

    const timestamp = new Date().toLocaleTimeString();

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: trimmed || "[Attachment]",
      timestamp,
      attachments: attachedFiles.map((f) => ({
        name: f.name,
        size: f.size,
        type: f.type,
      })),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    clearAttachments();
    setLoading(true);

    try {
      // optional: include attachment names in prompt context
      const attachmentSummary =
        userMessage.attachments?.length
          ? "\nUser also attached: " +
            userMessage.attachments.map((a) => a.name).join(", ")
          : "";

      // build history for AI
      const apiMessages = [
        { role: "system", content: SYSTEM_PROMPT },
        ...messages.map((m) => ({
          role: m.sender === "user" ? "user" : "assistant",
          content:
            (m.text || "") +
            (m.attachments?.length
              ? "\n[Attachments: " +
                m.attachments.map((a) => a.name).join(", ") +
                "]"
              : ""),
        })),
        {
          role: "user",
          content: trimmed + attachmentSummary,
        },
      ];

      // --------- CHOOSE ONE: OPENAI or GEMINI ----------

      // Example: Gemini (text‑only) [web:80][web:83]
      const response = await axios.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        {
          contents: apiMessages.map((m) => ({
            role: m.role === "assistant" ? "model" : "user",
            parts: [{ text: m.content }],
          })),
        },
        {
          headers: {
            "Content-Type": "application/json",
            "x-goog-api-key": import.meta.env.VITE_GEMINI_API_KEY,
          },
        }
      );

      const botText =
        response.data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() ||
        "I'm here with you. Tell me more about how you feel.";

      const botMessage = {
        id: Date.now() + 1,
        sender: "bot",
        text: botText,
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error(err);
      const errorMessage = {
        id: Date.now() + 2,
        sender: "bot",
        text: "Sorry, I'm having trouble connecting right now. You can try again in a moment.",
        timestamp: new Date().toLocaleTimeString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // audio recording using MediaRecorder API [web:105][web:112]
  const startRecording = async () => {
    if (isRecording) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        const audioUrl = URL.createObjectURL(blob);

        const msg = {
          id: Date.now(),
          sender: "user",
          text: "[Voice note]",
          audioUrl,
          timestamp: new Date().toLocaleTimeString(),
        };

        setMessages((prev) => [...prev, msg]);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone", error);
      alert("Microphone access blocked. Please allow it in your browser.");
    }
  };

  const stopRecording = () => {
    if (!isRecording || !mediaRecorderRef.current) return;
    mediaRecorderRef.current.stop();
    mediaRecorderRef.current.stream.getTracks().forEach((t) => t.stop());
    setIsRecording(false);
  };

  const clearHistory = () => {
    localStorage.removeItem(STORAGE_KEY);
    setMessages([
      {
        id: 1,
        sender: "bot",
        text: "Hi, I'm MindEase. I'm here to listen. How are you feeling right now?",
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
  };

  return (
    <>
      {/* WELCOME OVERLAY */}
      {showWelcome && (
        <div className="welcome-overlay">
          <div className="welcome-logo">MindEase</div>
          <div className="welcome-text">Your emotional companion</div>
        </div>
      )}

      {/* FLOATING ORBS BACKGROUND */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>

      {/* THEME TOGGLE BUTTON - Bottom Right */}
      <button
        className="theme-toggle-btn"
        onClick={toggleTheme}
        aria-label={darkMode ? "Switch to light mode" : "Switch to dark mode"}
      >
        {darkMode ? "☀️" : "🌙"}
      </button>

      {/* MAIN CHAT INTERFACE */}
      <div className="chat-card">
        <div className="chat-header">
          <div>
            <h2 className="chat-title">MindEase - AI Companion </h2>
            <p className="chat-subtitle">
              Your feelings are valid. This space is just for you.
            </p>
          </div>
          <div className="chat-header-actions">
            <button className="history-btn" onClick={clearHistory}>
              Clear history
            </button>
            <span className="status-pill">Online</span>
          </div>
        </div>

        <div className="chat-window">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`message-row ${
                msg.sender === "user" ? "message-row-user" : "message-row-bot"
              }`}
            >
              {msg.sender === "bot" && <div className="avatar avatar-bot">M</div>}
              <div
                className={`message-bubble ${
                  msg.sender === "user" ? "bubble-user" : "bubble-bot"
                }`}
              >
                <p className="message-text">{msg.text}</p>

                {msg.audioUrl && (
                  <audio controls className="audio-player">
                    <source src={msg.audioUrl} type="audio/webm" />
                    Your browser does not support audio.
                  </audio>
                )}

                {msg.attachments && msg.attachments.length > 0 && (
                  <ul className="attachment-list">
                    {msg.attachments.map((a, idx) => (
                      <li key={idx} className="attachment-pill">
                        {a.name}
                      </li>
                    ))}
                  </ul>
                )}

                {/* REACTION BUTTONS - OPTIONAL */}
                <div className="message-reactions">
                  <button className="reaction-btn">💙</button>
                  <button className="reaction-btn">🤗</button>
                  <button className="reaction-btn">🌻</button>
                </div>

                <span className="message-time">{msg.timestamp}</span>
              </div>
              {msg.sender === "user" && (
                <div className="avatar avatar-user">You</div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message-row message-row-bot">
              <div className="avatar avatar-bot">M</div>
              <div className="message-bubble bubble-bot typing-bubble">
                <span className="dot" />
                <span className="dot" />
                <span className="dot" />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* ATTACHMENT PREVIEW */}
        {attachedFiles.length > 0 && (
          <div className="attachment-preview">
            <span>Attached:</span>
            {attachedFiles.map((f) => (
              <span key={f.name} className="attachment-pill">
                {f.name}
              </span>
            ))}
            <button className="clear-attachments-btn" onClick={clearAttachments}>
              ×
            </button>
          </div>
        )}

        {/* CHAT FOOTER */}
        <div className="chat-footer">
          {/* left: file attach */}
          <label className="icon-button">
            📎
            <input
              type="file"
              multiple
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </label>

          {/* center: textarea */}
          <textarea
            className="chat-input"
            placeholder="Share anything on your mind…"
            rows={2}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />

          {/* right: mic + send */}
          <div className="footer-right">
            <button
              type="button"
              className={`icon-button ${isRecording ? "recording" : ""}`}
              onMouseDown={startRecording}
              onMouseUp={stopRecording}
              onTouchStart={startRecording}
              onTouchEnd={stopRecording}
            >
              🎤
            </button>

            <button
              className="send-button"
              onClick={handleSend}
              disabled={loading || (!input.trim() && attachedFiles.length === 0)}
            >
              {loading ? "Sending..." : "Send"}
            </button>
          </div>
        </div>

        <p className="disclaimer">
          MindEase is for emotional support only and not a substitute for
          professional help or emergency services.
        </p>
        
        {/* FOOTER PATH NOTE */}
        <div className="footer-path-note">
          <small>
            Note: API key is valid for a limited time (typically 90 days). 
            For production use, set up a secure backend to handle API calls.
            Current endpoint: {import.meta.env.VITE_GEMINI_API_KEY ? "Gemini API" : "No API key configured"}
          </small>
        </div>
      </div>
    </>
  );
}

export default Chat;
