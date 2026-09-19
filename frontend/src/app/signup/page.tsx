"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { authApi } from "../../lib/api";
import { GlassCard } from "../../components/ui/GlassCard";

export default function SignupPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (authApi.isAuthenticated()) {
      router.replace("/chat");
    }
  }, [router]);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password || !confirmPassword) {
      setError("Please fill in all fields.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await authApi.signup(email.trim(), password);
      router.replace("/login?registered=true");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Signup failed. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: "100vh",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "var(--color-bg)",
      fontFamily: "var(--font-body)",
      position: "relative",
      overflow: "hidden",
    }}>
      {/* Animated background orbs */}
      <div style={{
        position: "absolute", top: "15%", left: "20%",
        width: 480, height: 480,
        background: "radial-gradient(circle, rgba(0,212,255,0.12) 0%, transparent 70%)",
        borderRadius: "50%", filter: "blur(40px)", pointerEvents: "none",
        animation: "orb1 8s ease-in-out infinite",
      }} />
      <div style={{
        position: "absolute", bottom: "10%", right: "15%",
        width: 420, height: 420,
        background: "radial-gradient(circle, rgba(123,97,255,0.15) 0%, transparent 70%)",
        borderRadius: "50%", filter: "blur(40px)", pointerEvents: "none",
        animation: "orb2 10s ease-in-out infinite",
      }} />
      <div style={{
        position: "absolute", top: "60%", left: "60%",
        width: 300, height: 300,
        background: "radial-gradient(circle, rgba(0,229,160,0.08) 0%, transparent 70%)",
        borderRadius: "50%", filter: "blur(30px)", pointerEvents: "none",
        animation: "orb1 12s ease-in-out infinite reverse",
      }} />

      <style>{`
        @keyframes orb1 {
          0%, 100% { transform: translateY(0px) scale(1); }
          50% { transform: translateY(-30px) scale(1.08); }
        }
        @keyframes orb2 {
          0%, 100% { transform: translateY(0px) scale(1); }
          50% { transform: translateY(25px) scale(0.94); }
        }
        @keyframes logoFloat {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-8px); }
        }
        @keyframes logoPulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(0,212,255,0.4); }
          50% { box-shadow: 0 0 0 16px rgba(0,212,255,0); }
        }
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(24px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes shake {
          0%,100% { transform: translateX(0); }
          20% { transform: translateX(-6px); }
          40% { transform: translateX(6px); }
          60% { transform: translateX(-4px); }
          80% { transform: translateX(4px); }
        }
        .login-input {
          width: 100%;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.1);
          border-radius: 10px;
          padding: 12px 16px;
          font-size: 14px;
          color: #F8FAFC;
          font-family: var(--font-body);
          outline: none;
          transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
          box-sizing: border-box;
        }
        .login-input::placeholder { color: #4A5568; }
        .login-input:focus {
          border-color: rgba(0,212,255,0.5);
          box-shadow: 0 0 0 3px rgba(0,212,255,0.12);
          background: rgba(0,212,255,0.04);
        }
        .login-input:hover:not(:focus) {
          border-color: rgba(255,255,255,0.2);
        }
        .login-btn {
          width: 100%;
          padding: 13px 24px;
          border: none;
          border-radius: 10px;
          background: linear-gradient(135deg, #00D4FF, #7B61FF);
          color: white;
          font-size: 15px;
          font-weight: 600;
          font-family: var(--font-body);
          cursor: pointer;
          transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
          position: relative;
          overflow: hidden;
          box-shadow: 0 4px 24px rgba(0,212,255,0.25);
        }
        .login-btn:hover:not(:disabled) {
          opacity: 0.92;
          transform: translateY(-1px);
          box-shadow: 0 8px 32px rgba(0,212,255,0.35);
        }
        .login-btn:active:not(:disabled) { transform: translateY(0px) scale(0.98); }
        .login-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .stat-chip {
          display: flex; align-items: center; gap: 6px;
          padding: 6px 12px; border-radius: 8px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          font-size: 11px; color: #64748B;
        }
        .stat-dot { width: 6px; height: 6px; border-radius: 50%; }
      `}</style>

      {/* Card */}
      <GlassCard style={{
        width: "100%", maxWidth: 440,
        margin: "0 20px",
        background: "rgba(14,22,33,0.85)",
        backdropFilter: "blur(24px)",
        WebkitBackdropFilter: "blur(24px)",
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: 20,
        padding: "40px 36px",
        boxShadow: "0 24px 80px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.06)",
        animation: mounted ? "fadeSlideUp 0.55s ease-out" : "none",
        position: "relative",
        overflow: "hidden",
      }}>
        {/* Card inner top shimmer */}
        <div style={{
          position: "absolute", top: 0, left: 0, right: 0, height: 1,
          background: "linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent)",
        }} />

        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: 32 }}>
          <div style={{
            width: 72, height: 72,
            borderRadius: 18,
            background: "linear-gradient(135deg, #00D4FF, #7B61FF)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 32, margin: "0 auto 16px",
            animation: "logoFloat 3s ease-in-out infinite, logoPulse 3s ease-in-out infinite",
            boxShadow: "0 8px 32px rgba(0,212,255,0.3)",
          }}>🧠</div>
          <h1 style={{
            fontFamily: "var(--font-display)",
            fontSize: 26, fontWeight: 700,
            background: "linear-gradient(135deg, #00D4FF, #7B61FF)",
            WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            backgroundClip: "text", marginBottom: 6, letterSpacing: "-0.03em",
          }}>HealthTech RAG</h1>
          <p style={{ color: "#64748B", fontSize: 13 }}>Create your account</p>
        </div>

        <form onSubmit={handleSignup} style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {/* Email */}
          <div>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#94A3B8", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Email
            </label>
            <input
              id="email"
              type="email"
              className="login-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              autoComplete="email"
            />
          </div>

          {/* Password */}
          <div>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#94A3B8", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              className="login-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="•••••••• (min 8 chars)"
              autoComplete="new-password"
            />
          </div>

          {/* Confirm Password */}
          <div>
            <label style={{ display: "block", fontSize: 11, fontWeight: 600, color: "#94A3B8", marginBottom: 8, textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              className="login-input"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              autoComplete="new-password"
            />
          </div>

          {/* Error */}
          {error && (
            <div style={{
              fontSize: 12, color: "#FF4D6A",
              background: "rgba(255,77,106,0.08)",
              border: "1px solid rgba(255,77,106,0.2)",
              borderRadius: 10, padding: "10px 14px",
              animation: "shake 0.4s ease",
            }}>
              ⚠️ {error}
            </div>
          )}

          {/* Submit */}
          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8 }}>
                <span style={{ display: "inline-block", animation: "spin 0.8s linear infinite" }}>⏳</span>
                Creating account…
              </span>
            ) : "Create Account →"}
          </button>
        </form>

        {/* Login link */}
        <div style={{ marginTop: 24, textAlign: "center", fontSize: 13, color: "#94A3B8" }}>
          Already have an account? <Link href="/login" style={{ color: "#00D4FF", textDecoration: "none", fontWeight: 500 }}>Sign in</Link>
        </div>

        {/* Footer stats */}
        <div style={{ marginTop: 28, display: "flex", justifyContent: "center", gap: 10, flexWrap: "wrap" }}>
          <div className="stat-chip">
            <div className="stat-dot" style={{ background: "#00E5A0" }} />
            <span>Ollama Running</span>
          </div>
          <div className="stat-chip">
            <div className="stat-dot" style={{ background: "#00D4FF" }} />
            <span>llama3.2</span>
          </div>
          <div className="stat-chip">
            <div className="stat-dot" style={{ background: "#7B61FF" }} />
            <span>ChromaDB</span>
          </div>
        </div>
      </GlassCard>
    </div>
  );
}