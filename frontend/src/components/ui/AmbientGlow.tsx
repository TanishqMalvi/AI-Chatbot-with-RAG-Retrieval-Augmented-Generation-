import React from 'react';

type AmbientGlowProps = {
  color?: string;
  pulseSpeed?: number;
  active?: boolean;
  className?: string;
};

export const AmbientGlow = ({
  color = '#00D4FF', // default teal
  pulseSpeed = 1,
  active = false,
  className = ''
}: AmbientGlowProps) => {
  // The glow is created via CSS with the 'ambient-glow' base class
  // and configured with style-based data attributes
  const style = active
    ? {
      '--ambient-glow-color': color,
      '--animation-duration': `${3 / pulseSpeed}s`,
    } as React.CSSProperties
    : {};

  return (
    <div
      className={`ambient-glow ${active ? 'active' : ''} ${className}`}
      style={style}
    />
  );
};