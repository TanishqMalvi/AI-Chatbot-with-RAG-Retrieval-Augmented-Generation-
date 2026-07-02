import React from 'react';
import { motion } from 'framer-motion';

export const TypingIndicator = () => {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 5, padding: '4px 0' }}>
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={{ y: [0, -6, 0], opacity: [0.35, 1, 0.35] }}
          transition={{ duration: 0.9, repeat: Infinity, delay: i * 0.18, ease: 'easeInOut' }}
          style={{
            width: 8, height: 8, borderRadius: '50%',
            background: 'linear-gradient(135deg, #00D4FF, #7B61FF)',
            boxShadow: '0 0 6px rgba(0,212,255,0.5)',
          }}
        />
      ))}
      <span style={{ fontSize: 12, color: '#64748B', marginLeft: 6, fontFamily: 'var(--font-body)' }}>
        Thinking…
      </span>
    </div>
  );
};
