'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { cn } from '@/lib/utils';

interface CommandItem {
  label: string;
  description?: string;
  action: () => void;
  shortcut?: string;
}

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const router = useRouter();

  const commands: CommandItem[] = [
    {
      label: 'Dashboard',
      description: 'View your story overview',
      action: () => {
        router.push('/');
        setOpen(false);
      },
      shortcut: 'D',
    },
    {
      label: 'Characters',
      description: 'Manage your cast',
      action: () => {
        router.push('/characters');
        setOpen(false);
      },
      shortcut: 'C',
    },
    {
      label: 'Editor',
      description: 'Line-by-line editing',
      action: () => {
        router.push('/editor');
        setOpen(false);
      },
      shortcut: 'E',
    },
    {
      label: 'Pipeline',
      description: 'Editorial feedback',
      action: () => {
        router.push('/pipeline');
        setOpen(false);
      },
      shortcut: 'P',
    },
    {
      label: 'Analytics',
      description: 'View statistics',
      action: () => {
        router.push('/analytics');
        setOpen(false);
      },
      shortcut: 'A',
    },
  ];

  const filtered = commands.filter(cmd =>
    cmd.label.toLowerCase().includes(search.toLowerCase()) ||
    cmd.description?.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen(!open);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 glass-panel px-4 py-2 rounded-lg flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors z-30"
      >
        <span>⌘</span>
        <span>K</span>
      </button>
    );
  }

  return (
    <>
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
        onClick={() => setOpen(false)}
      />
      <div className="fixed top-1/3 left-1/2 -translate-x-1/2 w-full max-w-2xl z-50 animate-in fade-in slide-in-from-top-4 duration-200">
        <div className="glass-panel rounded-lg shadow-2xl">
          <div className="p-4 border-b border-border/50">
            <input
              autoFocus
              type="text"
              placeholder="Search commands..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-transparent text-foreground placeholder:text-muted-foreground outline-none"
            />
          </div>
          <div className="max-h-96 overflow-y-auto">
            {filtered.map((cmd, idx) => (
              <button
                key={idx}
                onClick={cmd.action}
                className="w-full px-4 py-3 text-left hover:bg-primary/10 flex items-center justify-between transition-colors border-b border-border/30 last:border-b-0"
              >
                <div>
                  <p className="font-medium text-foreground">{cmd.label}</p>
                  {cmd.description && (
                    <p className="text-xs text-muted-foreground mt-1">{cmd.description}</p>
                  )}
                </div>
                {cmd.shortcut && (
                  <kbd className="hidden sm:block text-xs px-2 py-1 rounded bg-border text-muted-foreground">
                    {cmd.shortcut}
                  </kbd>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
