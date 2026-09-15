import React, { HTMLAttributes } from 'react';
import { motion } from 'framer-motion';

type GlassCardProps = Omit<HTMLAttributes<HTMLDivElement>, 'onAnimationStart' | 'onAnimationEnd' | 'onAnimationIteration' | 'onAnimationCancel' | 'onDragStart' | 'onDragEnd' | 'onDrag' | 'onDragEnter' | 'onDragLeave' | 'onDragOver' | 'onDrop'> & { children: React.ReactNode };

export const GlassCard: React.FC<GlassCardProps> = (props) => {
  const { className = '', children, ...rest } = props;
  return (
    <motion.div
      className={`glass-panel ${className}`}
      initial={{ opacity: 0, scale: 0.97 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4, ease: [0.34, 1.56, 0.64, 1] }}
      {...rest}
    >
      {children}
    </motion.div>
  );
};
