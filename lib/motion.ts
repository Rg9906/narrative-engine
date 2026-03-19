export const springPhysics = {
  micro: {
    duration: 0.15,
    bounce: 0.4,
  },
  small: {
    duration: 0.3,
    bounce: 0.35,
  },
  default: {
    duration: 0.5,
    bounce: 0.3,
  },
  major: {
    duration: 0.8,
    bounce: 0.25,
  },
};

export const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: springPhysics.default,
};

export const fadeInScale = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 },
  transition: springPhysics.small,
};

export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.08,
      delayChildren: 0.1,
    },
  },
};

export const staggerItem = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  transition: springPhysics.small,
};

export const glowPulse = {
  animate: {
    boxShadow: [
      '0 0 20px rgba(45, 90, 255, 0.3)',
      '0 0 40px rgba(45, 90, 255, 0.5)',
      '0 0 20px rgba(45, 90, 255, 0.3)',
    ],
  },
  transition: {
    duration: 3,
    repeat: Infinity,
    ease: 'easeInOut',
  },
};

export const cursorProximity = {
  hover: {
    scale: 1.05,
    boxShadow: '0 8px 32px rgba(45, 90, 255, 0.4)',
    y: -2,
  },
  transition: springPhysics.micro,
};

export const shimmer = {
  animate: {
    backgroundPosition: ['0% 0%', '100% 100%', '0% 0%'],
  },
  transition: {
    duration: 3,
    repeat: Infinity,
    ease: 'linear',
  },
};
