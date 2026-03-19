'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

interface NavItem {
  icon: string;
  label: string;
  href: string;
  active?: boolean;
}

const navItems: NavItem[] = [
  { icon: '◆', label: 'Dashboard', href: '/', active: true },
  { icon: '⚙', label: 'Characters', href: '/characters' },
  { icon: '✎', label: 'Editor', href: '/editor' },
  { icon: '◇', label: 'Pipeline', href: '/pipeline' },
  { icon: '⊡', label: 'Analytics', href: '/analytics' },
  { icon: '⚡', label: 'Settings', href: '/settings' },
];

export function LeftNavRail() {
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);
  const pathname = usePathname();

  return (
    <nav className="glass-panel w-20 h-screen fixed left-0 top-0 flex flex-col items-center justify-start py-8 border-r gap-4 z-50">
      {/* Logo/Branding */}
      <motion.div 
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ type: 'spring', stiffness: 200, damping: 20 }}
        whileHover={{ scale: 1.1, rotate: 5 }}
        className="w-12 h-12 rounded-lg glass-panel flex items-center justify-center mb-8 glow-primary"
      >
        <span className="text-xl font-serif font-bold text-primary">N</span>
      </motion.div>

      {/* Navigation items */}
      <div className="flex flex-col gap-3">
        {navItems.map((item, idx) => (
          <motion.div
            key={item.href}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.05, type: 'spring', stiffness: 300, damping: 30 }}
          >
            <Link
              href={item.href}
              onMouseEnter={() => setHoveredItem(item.label)}
              onMouseLeave={() => setHoveredItem(null)}
              className={cn(
                'w-12 h-12 rounded-lg flex items-center justify-center',
                'text-xl relative group',
                pathname === item.href
                  ? 'glass-panel glow-primary text-primary'
                  : 'hover:glass-panel text-muted-foreground hover:text-accent'
              )}
            >
              <motion.span
                whileHover={{ scale: 1.15, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
              >
                {item.icon}
              </motion.span>

              {/* Tooltip */}
              <AnimatePresence>
                {hoveredItem === item.label && (
                  <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -10 }}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                    className="absolute left-16 bg-card/95 backdrop-blur-sm border border-border rounded-lg px-3 py-2 text-xs whitespace-nowrap"
                  >
                    {item.label}
                  </motion.div>
                )}
              </AnimatePresence>
            </Link>
          </motion.div>
        ))}
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Bottom action */}
      <button
        className={cn(
          'w-12 h-12 rounded-lg flex items-center justify-center',
          'glass-panel text-muted-foreground hover:text-destructive hover:glow-accent',
          'transition-all duration-300 group'
        )}
      >
        <span className="text-lg">⊗</span>
      </button>
    </nav>
  );
}
