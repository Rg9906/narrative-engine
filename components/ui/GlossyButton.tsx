import React from 'react';
import { cn } from '@/lib/utils';

interface GlossyButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function GlossyButton({
  variant = 'primary',
  size = 'md',
  className,
  children,
  ...props
}: GlossyButtonProps) {
  const baseStyles =
    'relative font-medium rounded-lg transition-all duration-300 font-sans';

  const variantStyles = {
    primary:
      'bg-gradient-to-br from-primary to-purple-600 text-primary-foreground hover:shadow-lg hover:shadow-primary/40 active:scale-95',
    secondary:
      'bg-secondary text-secondary-foreground hover:bg-secondary/80 active:scale-95',
    accent:
      'bg-gradient-to-br from-accent to-cyan-400 text-accent-foreground hover:shadow-lg hover:shadow-accent/40 active:scale-95',
    ghost:
      'border border-border text-foreground hover:bg-muted hover:border-border/80 active:scale-95',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
      {...props}
    >
      {/* Glass shine effect */}
      <div className="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-30 bg-gradient-to-br from-white/40 to-transparent transition-opacity duration-300" />
      <span className="relative z-10 flex items-center justify-center gap-2">{children}</span>
    </button>
  );
}
