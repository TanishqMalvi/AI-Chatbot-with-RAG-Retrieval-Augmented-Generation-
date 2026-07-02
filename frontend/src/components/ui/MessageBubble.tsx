import React, { useState } from 'react';
import { motion } from 'framer-motion';

export type MessageBubbleProps = {
  type: 'user' | 'assistant';
  content: string;
  author?: string | null;
  timestamp?: Date;
  sources?: any[];
};

export const MessageBubble = ({ type, content, author, timestamp, sources }: MessageBubbleProps) => {
  const isUser = type === 'user';
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 16, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: 'spring', stiffness: 300, damping: 28 }}
      style={{
        display: 'flex',
        gap: 10,
        maxWidth: '82%',
        marginLeft: isUser ? 'auto' : undefined,
        flexDirection: isUser ? 'row-reverse' : 'row',
        alignItems: 'flex-start',
      }}
    >
      {/* Avatar */}
      <div style={{
        width: 34, height: 34, borderRadius: 10, flexShrink: 0,
        background: isUser
          ? 'linear-gradient(135deg, #00D4FF, #7B61FF)'
          : 'rgba(255,255,255,0.06)',
        border: isUser ? 'none' : '1px solid rgba(255,255,255,0.1)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: 16,
      }}>
        {isUser ? '👤' : '🧠'}
      </div>

      {/* Bubble */}
      <div style={{
        position: 'relative',
        padding: '12px 16px',
        borderRadius: isUser ? '18px 6px 18px 18px' : '6px 18px 18px 18px',
        background: isUser
          ? 'linear-gradient(135deg, #00D4FF, #7B61FF)'
          : 'rgba(255,255,255,0.05)',
        border: isUser ? 'none' : '1px solid rgba(255,255,255,0.08)',
        backdropFilter: isUser ? 'none' : 'blur(12px)',
        boxShadow: isUser
          ? '0 4px 20px rgba(0,212,255,0.2)'
          : '0 4px 20px rgba(0,0,0,0.3)',
        minWidth: 60,
      }}>
        {/* Author + time */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 8,
          marginBottom: 6, fontSize: 11,
          color: isUser ? 'rgba(255,255,255,0.7)' : '#64748B',
        }}>
          <span style={{ fontWeight: 600 }}>
            {isUser ? (author || 'You') : 'HealthTech AI'}
          </span>
          {timestamp && (
            <span>{timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
          )}
        </div>

        {/* Content */}
        <div style={{
          fontSize: 14, lineHeight: 1.65,
          color: isUser ? '#fff' : '#CBD5E1',
          whiteSpace: 'pre-wrap', wordBreak: 'break-word',
          fontFamily: isUser ? 'var(--font-body)' : 'var(--font-body)',
        }}>
          {content}
        </div>

        {/* Sources */}
        {sources && sources.length > 0 && (
          <div style={{
            marginTop: 10, paddingTop: 10,
            borderTop: '1px solid rgba(255,255,255,0.08)',
            display: 'flex', flexWrap: 'wrap', gap: 6,
          }}>
            <span style={{ fontSize: 11, color: '#64748B', width: '100%', marginBottom: 2 }}>Sources:</span>
            {sources.map((src, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                style={{
                  background: 'rgba(0,212,255,0.08)',
                  border: '1px solid rgba(0,212,255,0.25)',
                  borderRadius: 6, padding: '3px 8px',
                  fontSize: 11, color: '#00D4FF',
                }}
              >
                📄 {typeof src === 'string' ? src : src.filename || src.doc_id || `source ${i + 1}`}
              </motion.div>
            ))}
          </div>
        )}

        {/* Copy button (AI only) */}
        {!isUser && (
          <button
            onClick={handleCopy}
            title="Copy response"
            style={{
              position: 'absolute', top: 10, right: 10,
              background: copied ? 'rgba(0,229,160,0.15)' : 'rgba(255,255,255,0.05)',
              border: `1px solid ${copied ? 'rgba(0,229,160,0.3)' : 'rgba(255,255,255,0.1)'}`,
              borderRadius: 6, padding: '3px 8px',
              fontSize: 11, color: copied ? '#00E5A0' : '#64748B',
              cursor: 'pointer', transition: 'all 0.2s', fontFamily: 'var(--font-body)',
            }}
          >
            {copied ? '✓ Copied' : '📋'}
          </button>
        )}
      </div>
    </motion.div>
  );
};
