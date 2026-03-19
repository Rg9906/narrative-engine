# Developer Guide - Narrative Engine

## Getting Started

### Installation
```bash
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

### Project Structure
- `/app` - Next.js app router pages and layout
- `/components` - Reusable React components organized by feature
- `/lib` - Utilities, context, motion presets
- `/public` - Static assets

## Key Technologies

### Styling
- **Tailwind CSS v4**: Utility-first CSS framework
- **Custom CSS Variables**: Color system defined in `app/globals.css`
- **Glassmorphism**: Native CSS backdrop-filter for glass effect

### Animation
- **Framer Motion v11**: React animation library
  - All components use spring physics: `stiffness: 300, damping: 30`
  - Smooth hover, tap, and entrance animations
  - See animation patterns in enhanced components

### Components
- **shadcn/ui**: Pre-built accessible components (customizable)
- **Recharts**: Data visualization library for charts
- **React Hook Form**: Form state management
- **Zod**: TypeScript-first schema validation

## Component Patterns

### Adding Framer Motion to a Component

```tsx
'use client';
import { motion } from 'framer-motion';

function MyComponent() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      whileHover={{ scale: 1.05, y: -5 }}
    >
      Content
    </motion.div>
  );
}
```

### Staggered Container Pattern

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
};

<motion.div variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => <Item key={item.id} item={item} />)}
</motion.div>
```

## State Management

### App Context
The `AppContext` provides access to:
- `chapters` - Story chapters
- `characters` - Character roster
- Various UI state helpers

Located in `/lib/context/AppContext.tsx`

### Usage
```tsx
import { useAppContext } from '@/lib/context/AppContext';

function MyComponent() {
  const { chapters, characters } = useAppContext();
  // ...
}
```

## Color System

All colors are defined as CSS variables in `app/globals.css`:

```css
--background: #0B0F14        /* Deep graphite */
--foreground: #E8E9EB        /* Light text */
--primary: #2D5AFF           /* Electric blue */
--accent: #00D9FF            /* Cyan */
--chart-1: #2D5AFF           /* Blue chart */
--chart-2: #06D6D0           /* Teal chart */
```

Use in components:
```tsx
className="text-primary bg-secondary"
```

## Typography

The project uses:
- **Serif (headings)**: `font-serif` class applies Georgia/Garamond
- **Sans-serif (body)**: `font-sans` class applies Geist
- **Monospace (code)**: `font-mono` class applies Geist Mono

## Responsive Breakpoints

Tailwind breakpoints:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

Example: `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`

## Common Utilities

### Glass Panel
Apply consistent styling:
```tsx
className="glass-panel p-6 rounded-xl"
```

Includes: backdrop blur, semi-transparent background, subtle border

### Glow Effects
```tsx
className="glow-primary"  // Primary glow
className="glow-accent"   // Accent glow
```

### Text Balance
For better typography:
```tsx
className="text-balance"  // Breaks lines intelligently
```

## Navigation

### Pages Available
- `/` - Dashboard
- `/characters` - Character system
- `/editor` - Line editor
- `/pipeline` - Editorial pipeline
- `/analytics` - Analytics dashboard
- `/settings` - Settings

### Command Palette
Press `⌘K` (or `Ctrl+K`) to open the command palette with keyboard navigation.

## Adding a New Feature

### Step 1: Create the Component
```tsx
// components/my-feature/MyComponent.tsx
'use client';

import { motion } from 'framer-motion';

export function MyComponent() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      Content
    </motion.div>
  );
}
```

### Step 2: Add to Page
```tsx
// app/my-route/page.tsx
'use client';

import { WorkspaceLayout } from '@/components/layout/WorkspaceLayout';
import { PageHeader } from '@/components/common/PageHeader';
import { MyComponent } from '@/components/my-feature/MyComponent';

export default function Page() {
  return (
    <WorkspaceLayout>
      <PageHeader title="My Feature" subtitle="Description" icon="◆" />
      <MyComponent />
    </WorkspaceLayout>
  );
}
```

## Performance Tips

1. **Use `'use client'` sparingly** - Keep server components where possible
2. **Memoize expensive components** - Use `React.memo` for list items
3. **Lazy load heavy components** - Use `next/dynamic` with ssr: false
4. **Optimize animations** - Use transform and opacity only for 60fps
5. **Image optimization** - Use `next/image` with proper sizes

## Debugging

### Enable Debug Logs
Add console.log statements with `[v0]` prefix for visibility:
```tsx
console.log("[v0] MyComponent state:", state);
```

### Check Framer Motion
Ensure components are wrapped with motion:
```tsx
import { motion } from 'framer-motion';
// Use motion.div, motion.button, etc.
```

### Network Issues
Check browser DevTools Network tab for failed requests or slow loading.

## Building for Production

```bash
npm run build
npm start
```

The build process:
1. Compiles TypeScript
2. Bundles with Webpack/Turbopack
3. Optimizes images and assets
4. Creates optimized production bundle

## Deployment

### Vercel (Recommended)
```bash
vercel deploy
```

### Self-hosted
```bash
npm run build
npm start
```

Server will run on port 3000

## Troubleshooting

### CSS Not Loading
- Clear `.next` folder: `rm -rf .next`
- Restart dev server
- Check `app/globals.css` has no external imports

### Components Not Showing
- Ensure `'use client'` directive if using hooks
- Check imports are correct
- Verify component is exported

### Animation Jank
- Use transform/opacity only
- Avoid animating dimensions or position
- Check browser DevTools Performance tab

### State Not Updating
- Verify context is wrapped in AppProvider
- Check component is using useAppContext hook
- Ensure state setter is called correctly

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [shadcn/ui](https://ui.shadcn.com)
- [Recharts](https://recharts.org)

## Support

For issues or questions:
1. Check existing documentation
2. Review similar components for patterns
3. Check browser console for errors
4. Review git history for similar implementations
