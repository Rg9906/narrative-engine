'use client';

import React, { useRef, useEffect, useState } from 'react';
import { cn } from '@/lib/utils';

interface Node {
  id: string;
  name: string;
  color: string;
  x: number;
  y: number;
}

interface Link {
  source: string;
  target: string;
  type: 'allies' | 'enemies' | 'romantic' | 'family';
}

const nodes: Node[] = [
  { id: '1', name: 'Elena', color: '#06D6D0', x: 0.5, y: 0.3 },
  { id: '2', name: 'Marcus', color: '#EF4444', x: 0.8, y: 0.5 },
  { id: '3', name: 'Sophia', color: '#10B981', x: 0.2, y: 0.6 },
  { id: '4', name: 'James', color: '#F59E0B', x: 0.5, y: 0.8 },
];

const links: Link[] = [
  { source: '1', target: '2', type: 'enemies' },
  { source: '1', target: '3', type: 'family' },
  { source: '1', target: '4', type: 'allies' },
  { source: '3', target: '4', type: 'allies' },
  { source: '2', target: '3', type: 'enemies' },
];

const linkTypeStyles = {
  allies: { stroke: '#10B981', strokeDasharray: '0', label: '━' },
  enemies: { stroke: '#EF4444', strokeDasharray: '5,5', label: '✕' },
  romantic: { stroke: '#EC4899', strokeDasharray: '0', label: '♡' },
  family: { stroke: '#8B5CF6', strokeDasharray: '0', label: '⊗' },
};

export function CharacterRelationshipGraph() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoveredNode, setHoveredNode] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || !containerRef.current) return;

    const rect = containerRef.current.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.fillStyle = '#0B0F14';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw links first (so they appear behind nodes)
    links.forEach((link) => {
      const sourceNode = nodes.find((n) => n.id === link.source);
      const targetNode = nodes.find((n) => n.id === link.target);
      if (!sourceNode || !targetNode) return;

      const x1 = sourceNode.x * canvas.width;
      const y1 = sourceNode.y * canvas.height;
      const x2 = targetNode.x * canvas.width;
      const y2 = targetNode.y * canvas.height;

      const style = linkTypeStyles[link.type];

      ctx.strokeStyle = style.stroke;
      ctx.lineWidth = hoveredNode === link.source || hoveredNode === link.target ? 3 : 2;
      ctx.setLineDash(style.strokeDasharray.split(',').map(Number));

      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.stroke();

      ctx.setLineDash([]);
    });

    // Draw nodes
    nodes.forEach((node) => {
      const x = node.x * canvas.width;
      const y = node.y * canvas.height;
      const radius = hoveredNode === node.id ? 32 : 24;

      // Glow effect
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2);
      gradient.addColorStop(0, `${node.color}40`);
      gradient.addColorStop(1, `${node.color}00`);
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(x, y, radius * 2, 0, Math.PI * 2);
      ctx.fill();

      // Node circle
      ctx.fillStyle = node.color;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fill();

      // Node border
      ctx.strokeStyle = '#E8E9EB';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.stroke();

      // Node label
      ctx.fillStyle = '#0B0F14';
      ctx.font = 'bold 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(node.name.substring(0, 1), x, y);
    });
  }, [hoveredNode]);

  const handleCanvasHover = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    let hoveredId: string | null = null;

    nodes.forEach((node) => {
      const nodeX = node.x * canvas.width;
      const nodeY = node.y * canvas.height;
      const distance = Math.sqrt((x - nodeX) ** 2 + (y - nodeY) ** 2);

      if (distance < 40) {
        hoveredId = node.id;
      }
    });

    setHoveredNode(hoveredId);
  };

  return (
    <div ref={containerRef} className="glass-panel rounded-xl p-6 overflow-hidden h-80">
      <h3 className="text-lg font-serif font-bold text-foreground mb-4">Character Relationships</h3>

      <canvas
        ref={canvasRef}
        onMouseMove={handleCanvasHover}
        onMouseLeave={() => setHoveredNode(null)}
        className="w-full h-64 cursor-pointer"
      />

      {/* Legend */}
      <div className="flex flex-wrap gap-3 mt-4 text-xs">
        {(Object.entries(linkTypeStyles) as [string, (typeof linkTypeStyles)[keyof typeof linkTypeStyles]][]).map(
          ([type, style]) => (
            <div key={type} className="flex items-center gap-2">
              <div
                className="w-3 h-0.5"
                style={{
                  backgroundColor: style.stroke,
                  borderBottom: `2px ${type === 'enemies' ? 'dashed' : 'solid'} ${style.stroke}`,
                }}
              />
              <span className="text-muted-foreground capitalize">{type}</span>
            </div>
          )
        )}
      </div>
    </div>
  );
}
