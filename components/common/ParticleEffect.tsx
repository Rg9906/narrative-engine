'use client';

import React, { useEffect, useRef } from 'react';

interface ParticleConfig {
  count: number;
  colors: string[];
  speed: number;
  size: number;
}

const defaultConfig: ParticleConfig = {
  count: 30,
  colors: ['#2D5AFF', '#00D9FF', '#A855F7', '#06D6D0'],
  speed: 0.5,
  size: 2,
};

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  radius: number;
  opacity: number;
}

export function ParticleEffect({
  config = defaultConfig,
  className = '',
}: {
  config?: Partial<ParticleConfig>;
  className?: string;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animationIdRef = useRef<number>();

  const finalConfig = { ...defaultConfig, ...config };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Initialize particles
    particlesRef.current = Array.from({ length: finalConfig.count }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * finalConfig.speed,
      vy: (Math.random() - 0.5) * finalConfig.speed,
      color: finalConfig.colors[Math.floor(Math.random() * finalConfig.colors.length)],
      radius: finalConfig.size,
      opacity: Math.random() * 0.5 + 0.3,
    }));

    const animate = () => {
      // Clear canvas
      ctx.fillStyle = 'rgba(11, 15, 20, 0)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Update and draw particles
      particlesRef.current.forEach((particle) => {
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.opacity = Math.max(0, particle.opacity - 0.005);

        // Wrap around edges
        if (particle.x < 0) particle.x = canvas.width;
        if (particle.x > canvas.width) particle.x = 0;
        if (particle.y < 0) particle.y = canvas.height;
        if (particle.y > canvas.height) particle.y = 0;

        // Draw particle with glow
        ctx.shadowColor = particle.color;
        ctx.shadowBlur = 8;
        ctx.fillStyle = particle.color;
        ctx.globalAlpha = particle.opacity;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
      });

      // Regenerate particles that faded out
      particlesRef.current.forEach((particle) => {
        if (particle.opacity <= 0) {
          particle.x = Math.random() * canvas.width;
          particle.y = Math.random() * canvas.height;
          particle.vx = (Math.random() - 0.5) * finalConfig.speed;
          particle.vy = (Math.random() - 0.5) * finalConfig.speed;
          particle.opacity = Math.random() * 0.5 + 0.3;
        }
      });

      animationIdRef.current = requestAnimationFrame(animate);
    };

    animate();

    const handleResize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }
    };
  }, [finalConfig]);

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none ${className}`}
    />
  );
}
