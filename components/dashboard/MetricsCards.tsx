'use client';

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface Metric {
  label: string;
  value: number;
  target: number;
  icon: string;
  gradient: string;
  unit: string;
}

const metrics: Metric[] = [
  {
    label: 'Total Words',
    value: 0,
    target: 47250,
    icon: '◆',
    gradient: 'from-blue-600 to-purple-600',
    unit: 'words',
  },
  {
    label: 'Chapters',
    value: 0,
    target: 12,
    icon: '⚙',
    gradient: 'from-emerald-600 to-cyan-600',
    unit: 'chapters',
  },
  {
    label: 'Characters',
    value: 0,
    target: 8,
    icon: '✦',
    gradient: 'from-amber-600 to-yellow-600',
    unit: 'characters',
  },
  {
    label: 'Quality Score',
    value: 0,
    target: 92,
    icon: '⊡',
    gradient: 'from-pink-600 to-red-600',
    unit: '%',
  },
];

function AnimatedMetricCard({ metric }: { metric: Metric }) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const startTime = Date.now();
    const duration = 1200;

    const animateCount = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeOutQuad = 1 - (1 - progress) ** 2;
      setCount(Math.floor(metric.target * easeOutQuad));

      if (progress < 1) {
        requestAnimationFrame(animateCount);
      } else {
        setCount(metric.target);
      }
    };

    requestAnimationFrame(animateCount);
  }, [metric.target]);

  const percentage = (count / metric.target) * 100;

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      whileHover={{ scale: 1.05, y: -5 }}
      className="glass-panel p-6 rounded-xl group glow-accent"
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">{metric.label}</p>
          <div className="flex items-baseline gap-2 mt-2">
            <span className={cn('text-3xl font-serif font-bold bg-gradient-to-r', metric.gradient, 'bg-clip-text text-transparent')}>
              {count.toLocaleString()}
            </span>
            <span className="text-xs text-muted-foreground">{metric.unit}</span>
          </div>
        </div>
        <div className={cn('w-10 h-10 rounded-lg glass-panel flex items-center justify-center text-lg', 'bg-gradient-to-br', metric.gradient, 'text-white opacity-80')}>
          {metric.icon}
        </div>
      </div>

      {/* Progress bar */}
      <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
        <div
          className={cn('h-full bg-gradient-to-r', metric.gradient, 'rounded-full transition-all duration-500')}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>

      <p className="text-xs text-muted-foreground mt-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        {percentage.toFixed(0)}% of target
      </p>
    </motion.div>
  );
}

export function MetricsCards() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.05,
      },
    },
  };

  return (
    <motion.div 
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {metrics.map((metric) => (
        <AnimatedMetricCard key={metric.label} metric={metric} />
      ))}
    </motion.div>
  );
}
