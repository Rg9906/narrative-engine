'use client';

import React, { useEffect, useRef } from 'react';

export function CursorGlow() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mousePos = useRef({ x: 0, y: 0 });
  const lastPos = useRef({ x: 0, y: 0 });
  const trail = useRef<Array<{ x: number; y: number; opacity: number }>>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size to window
    const updateCanvasSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);

    // Track mouse position
    const handleMouseMove = (e: MouseEvent) => {
      mousePos.current = { x: e.clientX, y: e.clientY };
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Animation loop
    const animate = () => {
      // Add to trail
      trail.current.push({
        x: mousePos.current.x,
        y: mousePos.current.y,
        opacity: 1,
      });

      // Limit trail length
      if (trail.current.length > 20) {
        trail.current.shift();
      }

      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw trail with glow
      trail.current.forEach((point, index) => {
        const opacity = (index / trail.current.length) * 0.3;
        const size = 2 + (index / trail.current.length) * 8;

        // Draw glow
        ctx.shadowColor = '#2D5AFF';
        ctx.shadowBlur = 15;
        ctx.fillStyle = `rgba(45, 90, 255, ${opacity})`;
        ctx.beginPath();
        ctx.arc(point.x, point.y, size, 0, Math.PI * 2);
        ctx.fill();

        // Draw secondary glow
        ctx.shadowColor = '#00D9FF';
        ctx.shadowBlur = 8;
        ctx.fillStyle = `rgba(0, 217, 255, ${opacity * 0.5})`;
        ctx.beginPath();
        ctx.arc(point.x, point.y, size * 0.5, 0, Math.PI * 2);
        ctx.fill();
      });

      // Fade trail opacity
      trail.current.forEach((point) => {
        point.opacity -= 0.05;
      });

      requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', updateCanvasSize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-40"
      style={{ background: 'transparent' }}
    />
  );
}
