'use client';

import React, { useEffect, useRef } from 'react';

interface DataPoint {
  label: string;
  value: number;
  color: string;
}

interface RadarChartProps {
  data: DataPoint[];
  size?: number;
}

export function RadarChart({ data, size = 300 }: RadarChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 40;
    const levels = 5;
    const angleSlice = (Math.PI * 2) / data.length;

    // Clear canvas
    ctx.fillStyle = '#0B0F14';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw concentric circles (levels)
    ctx.strokeStyle = 'rgba(42, 47, 57, 0.3)';
    ctx.lineWidth = 1;

    for (let i = 1; i <= levels; i++) {
      const r = (radius / levels) * i;
      ctx.beginPath();
      ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Draw axes and labels
    data.forEach((point, i) => {
      const angle = angleSlice * i - Math.PI / 2;
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);

      // Axis line
      ctx.strokeStyle = 'rgba(42, 47, 57, 0.5)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.lineTo(x, y);
      ctx.stroke();

      // Label
      ctx.fillStyle = '#8A8F99';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      const labelRadius = radius + 30;
      const labelX = centerX + labelRadius * Math.cos(angle);
      const labelY = centerY + labelRadius * Math.sin(angle);
      ctx.fillText(point.label, labelX, labelY);
    });

    // Draw data polygon
    ctx.fillStyle = 'rgba(45, 90, 255, 0.15)';
    ctx.strokeStyle = '#2D5AFF';
    ctx.lineWidth = 2;
    ctx.beginPath();

    data.forEach((point, i) => {
      const angle = angleSlice * i - Math.PI / 2;
      const value = Math.max(0, Math.min(100, point.value));
      const r = (radius / 100) * value;
      const x = centerX + r * Math.cos(angle);
      const y = centerY + r * Math.sin(angle);

      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });

    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Draw data points
    data.forEach((point, i) => {
      const angle = angleSlice * i - Math.PI / 2;
      const value = Math.max(0, Math.min(100, point.value));
      const r = (radius / 100) * value;
      const x = centerX + r * Math.cos(angle);
      const y = centerY + r * Math.sin(angle);

      ctx.fillStyle = point.color;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = '#E8E9EB';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.stroke();
    });
  }, [data]);

  return (
    <div ref={containerRef} className="w-full h-64">
      <canvas ref={canvasRef} className="w-full h-full" />
    </div>
  );
}
