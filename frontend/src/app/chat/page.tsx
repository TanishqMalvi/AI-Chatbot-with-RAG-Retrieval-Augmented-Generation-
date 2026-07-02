"use client";
import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { authApi, chatApi } from "../../lib/api";
import { Sidebar } from "../../components/ui/Sidebar";
import { MessageBubble } from "../../components/ui/MessageBubble";
import { TypingIndicator } from "../../components/ui/TypingIndicator";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: any[];
  timestamp: Date;
}
interface ChatResponse { answer: string; sources?: any[]; }

const SUGGESTIONS = [
  "What are the latest diabetes treatment protocols?",
  "Summarize hypertension guidelines",
  "Drug interaction for metformin",
  "COVID-19 long-term effects research",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const autoResize = () => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 130) + "px";
  };

  const handleSubmit = async (text?: string) => {
    const query = (text ?? input).trim();
    if (!query || isLoading) return;
    const userMsg: Message = { id: Date.now().toString(), role: "user", content: query, timestamp: new Date() };
    setMessages((p) => [...p, userMsg]);
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    setIsLoading(true);
    try {
      const history = [...messages, userMsg].map((m) => ({ role: m.role, content: m.content }));
      const data: ChatResponse = await chatApi.sendMessage(query, history, "hyde");
      setMessages((p) => [...p, {
        id: (Date.now() + 1).toString(), role: "assistant",
        content: data.answer, sources: data.sources ?? [], timestamp: new Date(),
      }]);
    } catch (err: unknown) {
      setMessages((p) => [...p, {
        id: (Date.now() + 1).toString(), role: "assistant",
        content: `⚠️ Error: ${err instanceof Error ? err.message : "Something went wrong."}`,
        timestamp: new Date(),
      }]);
    } finally { setIsLoading(false); }
  };

  const handleLogout = () => { authApi.logout(); window.location.href = "/login"; };

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden", background: "var(--color-bg)", fontFamily: "var(--font-body)", position: "relative" }}>
      <style>{`
        @keyframes orb-drift {
          0%,100% { transform: translateY(0) scale(1); }
          50% { transform: translateY(-20px) scale(1.05); }
        }
        @keyframes pulse-ring {
          0%,100% { box-shadow: 0 0 0 0 rgba(0,212,255,0.4); }
          50% { box-shadow: 0 0 0 10px rgba(0,212,255,0); }
        }
        @keyframes fadeUp {
          from { opacity:0; transform: translateY(16px); }
          to { opacity:1; transform: translateY(0); }
        }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

        .chat-textarea {
          flex: 1; background: transparent; border: none; outline: none;
          font-size: 14px; color: #F8FAFC; resize: none;
          font-family: var(--font-body); line-height: 1.6;
          max-height: 130px; padding: 2px 0;
        }
        .chat-textarea::placeholder { color: #475569; }
        .send-btn {
          width: 40px; height: 40px; border-radius: 10px; border: none;
          background: linear-gradient(135deg, #00D4FF, #7B61FF);
          color: white; font-size: 16px; cursor: pointer;
          display: flex; align-items: center; justify-content: center;
          flex-shrink: 0; transition: opacity 0.2s, transform 0.15s;
          box-shadow: 0 4px 16px rgba(0,212,255,0.3);
        }
        .send-btn:hover:not(:disabled) { opacity: 0.88; transform: scale(1.06); }
        .send-btn:active:not(:disabled) { transform: scale(0.95); }
        .send-btn:disabled { background: rgba(255,255,255,0.06); box-shadow: none; cursor: not-allowed; }
        .suggestion-btn {
          padding: 8px 14px; border-radius: 999px;
          border: 1px solid rgba(255,255,255,0.1);
          background: rgba(255,255,255,0.04);
          color: #94A3B8; font-size: 12px; cursor: pointer;
          font-family: var(--font-body); white-space: nowrap;
          transition: all 0.2s;
        }
        .suggestion-btn:hover {
          background: rgba(0,212,255,0.08);
          border-color: rgba(0,212,255,0.3); color: #CBD5E1;
        }
        .status-dot { width: 7px; height: 7px; border-radius: 50%; background: #00E5A0; display: inline-block; animation: pulse-ring 2.5s ease-in-out infinite; }
      `}</style>

      {/* Background orbs */}
      <div style={{ position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none" }}>
        <div style={{ position: "absolute", top: "10%", right: "15%", width: 500, height: 500, borderRadius: "50%", background: "radial-gradient(circle, rgba(0,212,255,0.07) 0%, transparent 70%)", filter: "blur(40px)", animation: "orb-drift 12s ease-in-out infinite" }} />
        <div style={{ position: "absolute", bottom: "15%", left: "20%", width: 400, height: 400, borderRadius: "50%", background: "radial-gradient(circle, rgba(123,97,255,0.08) 0%, transparent 70%)", filter: "blur(40px)", animation: "orb-drift 9s ease-in-out infinite reverse" }} />
      </div>

      {/* Sidebar */}
      <Sidebar onLogout={handleLogout} />

      {/* Main */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", position: "relative", zIndex: 1 }}>

        {/* Header */}
        <motion.header
          initial={{ y: -24, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.4 }}
          style={{
            display: "flex", alignItems: "center", justifyContent: "space-between",
            padding: "14px 24px",
            background: "rgba(8,12,20,0.7)",
            backdropFilter: "blur(20px)",
            WebkitBackdropFilter: "blur(20px)",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
            flexShrink: 0,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <motion.div
              animate={{ boxShadow: ["0 0 0 0 rgba(0,212,255,0.4)", "0 0 0 10px rgba(0,212,255,0)", "0 0 0 0 rgba(0,212,255,0.4)"] }}
              transition={{ duration: 2.5, repeat: Infinity }}
              style={{
                width: 40, height: 40, borderRadius: 10,
                background: "linear-gradient(135deg, #00D4FF, #7B61FF)",
                display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20,
              }}
            >🧠</motion.div>
            <div>
              <div style={{ fontSize: 16, fontWeight: 700, fontFamily: "var(--font-display)", background: "linear-gradient(135deg, #00D4FF, #7B61FF)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>
                HealthTech RAG
              </div>
              <div style={{ fontSize: 11, color: "#64748B" }}>AI-Powered Medical Assistant</div>
            </div>
          </div>

          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "5px 12px", borderRadius: 999, background: "rgba(0,229,160,0.08)", border: "1px solid rgba(0,229,160,0.2)", fontSize: 12, color: "#00E5A0" }}>
              <span className="status-dot" /> Connected
            </div>
            <div style={{ padding: "5px 12px", borderRadius: 8, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)", fontSize: 12, color: "#94A3B8" }}>
              👤 {authApi.getUserId()}
            </div>
            <button
              onClick={handleLogout}
              style={{
                padding: "5px 12px", borderRadius: 8, cursor: "pointer",
                background: "rgba(255,77,106,0.08)", border: "1px solid rgba(255,77,106,0.2)",
                fontSize: 12, color: "#FF4D6A", fontFamily: "var(--font-body)", transition: "all 0.2s",
              }}
              onMouseEnter={e => (e.currentTarget.style.background = "rgba(255,77,106,0.15)")}
              onMouseLeave={e => (e.currentTarget.style.background = "rgba(255,77,106,0.08)")}
            >↩ Logout</button>
          </div>
        </motion.header>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: "24px", display: "flex", flexDirection: "column", gap: 16 }}>
          <AnimatePresence>
            {messages.length === 0 && !isLoading && (
              <motion.div
                key="empty"
                initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", padding: "60px 20px", gap: 16 }}
              >
                <motion.div
                  animate={{ y: [0, -10, 0] }}
                  transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                  style={{
                    width: 72, height: 72, borderRadius: 18, fontSize: 32,
                    background: "linear-gradient(135deg, #00D4FF, #7B61FF)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    boxShadow: "0 8px 32px rgba(0,212,255,0.25)",
                  }}
                >🏥</motion.div>
                <div style={{ fontFamily: "var(--font-display)", fontSize: 22, fontWeight: 700, background: "linear-gradient(135deg, #00D4FF, #7B61FF)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>
                  Welcome!
                </div>
                <div style={{ fontSize: 14, color: "#64748B", maxWidth: 400, lineHeight: 1.7 }}>
                  Ask anything about medical research, clinical guidelines, or drug interactions.
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 8, justifyContent: "center", marginTop: 8 }}>
                  {SUGGESTIONS.map((s, i) => (
                    <button key={i} className="suggestion-btn" onClick={() => handleSubmit(s)}>{s}</button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              type={msg.role}
              content={msg.content}
              author={msg.role === "user" ? authApi.getUserId() : undefined}
              timestamp={msg.timestamp}
              sources={msg.sources}
            />
          ))}

          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              style={{ display: "flex", alignItems: "flex-start", gap: 10 }}
            >
              <div style={{ width: 34, height: 34, borderRadius: 10, background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, flexShrink: 0 }}>🧠</div>
              <div style={{ padding: "14px 18px", borderRadius: "6px 18px 18px 18px", background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)", backdropFilter: "blur(12px)" }}>
                <TypingIndicator />
              </div>
            </motion.div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <motion.div
          initial={{ y: 24, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.4 }}
          style={{
            padding: "16px 24px",
            background: "rgba(8,12,20,0.7)",
            backdropFilter: "blur(20px)",
            WebkitBackdropFilter: "blur(20px)",
            borderTop: "1px solid rgba(255,255,255,0.06)",
            flexShrink: 0,
          }}
        >
          <div style={{
            display: "flex", alignItems: "flex-end", gap: 12,
            background: "rgba(255,255,255,0.04)",
            border: "1px solid rgba(255,255,255,0.08)",
            borderRadius: 14, padding: "12px 14px",
            transition: "border-color 0.2s, box-shadow 0.2s",
            boxShadow: "0 4px 24px rgba(0,0,0,0.3)",
          }}
            onFocus={() => {}}
          >
            <textarea
              ref={textareaRef}
              className="chat-textarea"
              value={input}
              onChange={(e) => { setInput(e.target.value); autoResize(); }}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSubmit(); } }}
              placeholder="Ask about medical research, guidelines, drug interactions…"
              rows={1}
            />
            <button
              className="send-btn"
              onClick={() => handleSubmit()}
              disabled={isLoading || !input.trim()}
            >
              {isLoading
                ? <span style={{ display: "inline-block", animation: "spin 0.8s linear infinite" }}>⏳</span>
                : "→"}
            </button>
          </div>
          <div style={{ textAlign: "center", fontSize: 11, color: "#334155", marginTop: 8 }}>
            Enter to send · Shift+Enter for new line · Powered by RAG + HyDE + llama3.2
          </div>
        </motion.div>
      </div>
    </div>
  );
}
