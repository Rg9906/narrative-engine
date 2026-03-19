'use client';

import React, { useEffect, useState } from 'react';

export function ParallaxBackground() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 100,
        y: (e.clientY / window.innerHeight) * 100,
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none">
      {/* Deep base layer */}
      <div className="absolute inset-0 bg-gradient-to-br from-background via-[#0F141F] to-background opacity-100" />

      {/* Animated accent layers - positioned based on mouse movement */}
      <div
        className="absolute -inset-[40%] opacity-20 blur-3xl rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(45, 90, 255, 0.3) 0%, transparent 70%)',
          transform: `translate(${mousePosition.x * 0.05}%, ${mousePosition.y * 0.05}%)`,
          transition: 'transform 0.1s ease-out',
        }}
      />

      <div
        className="absolute -top-1/2 -right-1/4 w-96 h-96 opacity-10 blur-3xl rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(168, 85, 247, 0.4) 0%, transparent 70%)',
          transform: `translate(${-mousePosition.x * 0.03}%, ${-mousePosition.y * 0.03}%)`,
          transition: 'transform 0.15s ease-out',
        }}
      />

      <div
        className="absolute -bottom-1/3 -left-1/4 w-80 h-80 opacity-15 blur-3xl rounded-full"
        style={{
          background: 'radial-gradient(circle, rgba(0, 217, 255, 0.2) 0%, transparent 70%)',
          transform: `translate(${mousePosition.x * 0.04}%, ${mousePosition.y * 0.04}%)`,
          transition: 'transform 0.12s ease-out',
        }}
      />

      {/* Grid overlay for subtle structure */}
      <div className="absolute inset-0 opacity-5">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>
    </div>
  );
}
