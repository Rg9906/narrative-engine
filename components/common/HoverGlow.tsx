'use client';

import React, { useRef, useState } from 'react';

export function HoverGlow({
  children,
  glowColor = '#2D5AFF',
  intensity = 0.4,
  className = '',
}: {
  children: React.ReactNode;
  glowColor?: string;
  intensity?: number;
  className?: string;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    setMousePos({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
    });
  };

  const handleMouseEnter = () => {
    setIsHovering(true);
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
  };

  return (
    <div
      ref={containerRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className={`relative ${className}`}
      style={{
        position: 'relative',
        overflow: 'visible',
      }}
    >
      {isHovering && (
        <div
          style={{
            position: 'absolute',
            left: mousePos.x,
            top: mousePos.y,
            width: '100px',
            height: '100px',
            borderRadius: '50%',
            background: `radial-gradient(circle, ${glowColor}${Math.round(255 * intensity).toString(16).padStart(2, '0')}, transparent)`,
            filter: 'blur(30px)',
            pointerEvents: 'none',
            transform: 'translate(-50%, -50%)',
            zIndex: 1,
          }}
        />
      )}
      <div style={{ position: 'relative', zIndex: 2 }}>{children}</div>
    </div>
  );
}
