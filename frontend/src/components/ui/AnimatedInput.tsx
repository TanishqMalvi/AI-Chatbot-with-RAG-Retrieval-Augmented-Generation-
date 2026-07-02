import React from 'react';
import { motion } from 'framer-motion';

interface AnimatedInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export const AnimatedInput = ({ label, className = '', ...props }: AnimatedInputProps) => {
  return (
    <div className="relative">
      <label className="text-xs font-medium text-slate-400 mb-2 block">{label}</label>
      <motion.input
        whileFocus={{ scale: 1.01 }}
        className={`w-full bg-slate-950/30 border border-slate-700/50 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-300/80 transition-all duration-200 ${className}`}
        {...props}
      />
    </div>
  );
};
