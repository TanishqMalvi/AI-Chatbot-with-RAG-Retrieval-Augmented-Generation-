"use client";
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { authApi } from "../../lib/api";

interface SidebarProps { onLogout: () => void; }

const conversations = [
  { id: 1, title: "Diabetes Treatment Protocols", icon: "💉" },
  { id: 2, title: "Hypertension Guidelines", icon: "❤️" },
  { id: 3, title: "Drug Interaction Analysis", icon: "💊" },
];

export const Sidebar = ({ onLogout }: SidebarProps) => {
  const [collapsed, setCollapsed] = useState(false);
  const [activeConv, setActiveConv] = useState(1);
  const userId = authApi.getUserId() || "user";

  return (
    <>
      <style>{`
        .sidebar-conv-btn {
          width: 100%; padding: 10px 12px; border-radius: 10px;
          border: 1px solid transparent; background: rgba(255,255,255,0.03);
          color: #94A3B8; font-size: 13px; font-family: var(--font-body);
          cursor: pointer; text-align: left; transition: all 0.2s;
          display: flex; align-items: center; gap: 8px;
        }
        .sidebar-conv-btn:hover {
          background: rgba(0,212,255,0.06);
          border-color: rgba(0,212,255,0.2);
          color: #CBD5E1;
        }
        .sidebar-conv-btn.active {
          background: rgba(0,212,255,0.1);
          border-color: rgba(0,212,255,0.3);
          color: #00D4FF;
        }
        .sidebar-logout-btn {
          width: 100%; padding: 10px 12px; border-radius: 10px;
          border: 1px solid rgba(255,77,106,0.2);
          background: rgba(255,77,106,0.06);
          color: #FF4D6A; font-size: 13px; font-family: var(--font-body);
          cursor: pointer; display: flex; align-items: center;
          justify-content: center; gap: 6px;
          transition: all 0.2s; font-weight: 500;
        }
        .sidebar-logout-btn:hover {
          background: rgba(255,77,106,0.12);
          border-color: rgba(255,77,106,0.4);
        }
        .sidebar-toggle-btn {
          width: 36px; height: 36px; border-radius: 10px;
          border: 1px solid rgba(255,255,255,0.08);
          background: rgba(255,255,255,0.04);
          color: #94A3B8; font-size: 16px;
          cursor: pointer; display: flex;
          align-items: center; justify-content: center;
          transition: all 0.2s; margin-bottom: 20px;
        }
        .sidebar-toggle-btn:hover { background: rgba(255,255,255,0.08); color: #F8FAFC; }
      `}</style>

      <motion.aside
        animate={{ width: collapsed ? 64 : 260 }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
        style={{
          height: "100vh",
          flexShrink: 0,
          background: "rgba(8,12,20,0.8)",
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          borderRight: "1px solid rgba(255,255,255,0.06)",
          display: "flex",
          flexDirection: "column",
          padding: "20px 12px",
          overflow: "hidden",
          position: "relative",
        }}
      >
        {/* Top shimmer */}
        <div style={{
          position: "absolute", top: 0, left: 0, right: 0, height: 1,
          background: "linear-gradient(90deg, transparent, rgba(0,212,255,0.2), transparent)",
        }} />

        {/* Toggle */}
        <button className="sidebar-toggle-btn" onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? "→" : "☰"}
        </button>

        {/* User profile */}
        <AnimatePresence>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              style={{
                display: "flex", alignItems: "center", gap: 10,
                padding: "12px", borderRadius: 12,
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.07)",
                marginBottom: 24,
              }}
            >
              <div style={{
                width: 36, height: 36, borderRadius: "50%",
                background: "linear-gradient(135deg, #00D4FF, #7B61FF)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 16, flexShrink: 0,
              }}>👤</div>
              <div style={{ minWidth: 0 }}>
                <p style={{ fontSize: 13, fontWeight: 600, color: "#F8FAFC", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{userId}</p>
                <p style={{ fontSize: 11, color: "#64748B" }}>Healthcare Professional</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Conversations label */}
        <AnimatePresence>
          {!collapsed && (
            <motion.p
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              style={{ fontSize: 10, fontWeight: 700, color: "#475569", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 10, paddingLeft: 4 }}
            >
              Conversations
            </motion.p>
          )}
        </AnimatePresence>

        {/* Conversation list */}
        <div style={{ display: "flex", flexDirection: "column", gap: 4, flex: 1 }}>
          {conversations.map((c) => (
            <button
              key={c.id}
              className={`sidebar-conv-btn${activeConv === c.id ? " active" : ""}`}
              onClick={() => setActiveConv(c.id)}
              title={c.title}
            >
              <span style={{ flexShrink: 0 }}>{c.icon}</span>
              {!collapsed && (
                <span style={{ whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{c.title}</span>
              )}
            </button>
          ))}
        </div>

        {/* Logout */}
        <button className="sidebar-logout-btn" onClick={onLogout} title="Logout">
          <span>↩</span>
          {!collapsed && <span>Logout</span>}
        </button>
      </motion.aside>
    </>
  );
};
