# UI/UX Design System Guide

## Overview
This document outlines the design system, best practices, and UI/UX improvements implemented in the bobmarley application.

## Design Principles

### 1. Consistency
- Unified color palette across all components
- Consistent spacing and sizing using CSS variables
- Standardized border radius and shadows

### 2. Accessibility
- ARIA labels on all interactive elements
- Keyboard navigation support (Tab, Enter, Escape)
- Focus-visible states for keyboard users
- Proper color contrast ratios (WCAG AA compliant)
- Screen reader friendly status messages

### 3. Performance
- Smooth 60fps animations using CSS transforms
- Hardware-accelerated transitions
- Optimized re-renders with React best practices
- Lazy loading for heavy components

### 4. Responsiveness
- Mobile-first approach
- Breakpoints: 768px (tablet), 1024px (desktop)
- Flexible layouts that adapt to screen size
- Touch-friendly tap targets (min 48x48px)

## Color System

### Primary Colors
```css
--primary: #00d2ff (Cyan Blue)
--secondary: #8b5cf6 (Purple)
--accent: #06b6d4 (Cyan)
```

### Semantic Colors
```css
--success: #10b981 (Green)
--warning: #f59e0b (Amber)
--error: #ef4444 (Red)
```

### Neutral Colors
```css
--background: #0a0f19 (Dark Blue)
--text: #f3f4f6 (Light Gray)
--text-muted: #9ca3af (Medium Gray)
--text-dim: #6b7280 (Dim Gray)
```

### Glass Morphism
```css
--glass: rgba(255, 255, 255, 0.04)
--glass-border: rgba(255, 255, 255, 0.1)
--glass-hover: rgba(255, 255, 255, 0.08)
```

## Typography

### Font Stack
- Primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
- Monospace: 'Fira Code', 'Consolas', monospace

### Scale
- Heading 1: 3.5rem (56px) - Page titles
- Heading 2: 2rem (32px) - Section headers
- Heading 3: 1.5rem (24px) - Subsections
- Body: 1rem (16px) - Default text
- Small: 0.875rem (14px) - Captions
- Tiny: 0.75rem (12px) - Labels

## Spacing System

Using 8px base unit:
- xs: 0.5rem (8px)
- sm: 0.75rem (12px)
- md: 1rem (16px)
- lg: 1.5rem (24px)
- xl: 2rem (32px)
- 2xl: 3rem (48px)

## Border Radius

```css
--radius-sm: 8px
--radius-md: 12px
--radius-lg: 16px
--radius-xl: 24px
```

## Shadows

```css
--shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3)
--shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4)
--shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5)
--shadow-glow: 0 0 20px var(--primary-glow)
```

## Animation Timing

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1)
--transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1)
--transition-slow: 400ms cubic-bezier(0.4, 0, 0.2, 1)
```

## Component Patterns

### Glass Cards
```jsx
<div className="glass p-6 rounded-3xl">
  {/* Content */}
</div>
```

Features:
- Frosted glass effect with backdrop blur
- Subtle border and shadow
- Hover state with lift effect
- Smooth transitions

### Buttons

#### Primary Button
```jsx
<button style={{
  background: 'linear-gradient(135deg, #00d2ff, #8b5cf6)',
  color: '#fff',
  padding: '12px 24px',
  borderRadius: '12px',
  border: 'none',
  cursor: 'pointer',
  transition: 'all 0.25s',
}}>
  Action
</button>
```

#### Secondary Button
```jsx
<button style={{
  background: 'rgba(255,255,255,0.05)',
  border: '1px solid rgba(255,255,255,0.1)',
  color: '#fff',
  padding: '12px 24px',
  borderRadius: '12px',
  cursor: 'pointer',
}}>
  Action
</button>
```

### Input Fields
```jsx
<input 
  className="glass-input"
  placeholder="Enter text..."
  aria-label="Input description"
/>
```

Features:
- Glass morphism background
- Focus state with primary color border
- Smooth transitions
- Proper ARIA labels

### Status Indicators

#### Online/Offline Badge
```jsx
<div style={{
  display: 'flex',
  alignItems: 'center',
  gap: '8px'
}}>
  <span style={{
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#10b981',
    boxShadow: '0 0 8px #10b981'
  }} />
  <span>Online</span>
</div>
```

## Accessibility Checklist

### Keyboard Navigation
- [ ] All interactive elements are keyboard accessible
- [ ] Tab order is logical
- [ ] Focus states are visible
- [ ] Escape key closes modals/overlays
- [ ] Enter/Space activates buttons

### Screen Readers
- [ ] All images have alt text
- [ ] ARIA labels on icon-only buttons
- [ ] ARIA live regions for dynamic content
- [ ] Proper heading hierarchy
- [ ] Form labels associated with inputs

### Visual
- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] Focus indicators are visible
- [ ] No information conveyed by color alone
- [ ] Text is resizable up to 200%
- [ ] Touch targets ≥ 48x48px

## Responsive Breakpoints

### Mobile (< 768px)
- Single column layouts
- Stacked navigation
- Full-width components
- Larger touch targets

### Tablet (768px - 1024px)
- Two-column layouts where appropriate
- Collapsible sidebar
- Optimized spacing

### Desktop (> 1024px)
- Multi-column layouts
- Persistent sidebar option
- Hover states
- Keyboard shortcuts

## Performance Best Practices

### CSS
- Use CSS transforms for animations (not top/left)
- Leverage will-change for complex animations
- Minimize repaints and reflows
- Use CSS containment where appropriate

### React
- Memoize expensive computations
- Use React.memo for pure components
- Implement virtualization for long lists
- Lazy load routes and heavy components

### Images
- Use WebP format with fallbacks
- Implement lazy loading
- Provide appropriate sizes
- Use CSS for decorative elements

## Micro-interactions

### Hover Effects
- Scale: 1.05 for cards
- Lift: translateY(-4px) with shadow increase
- Color shift: Brighten by 10-20%
- Duration: 250ms

### Click/Tap Feedback
- Scale down: 0.98
- Duration: 150ms
- Immediate visual response

### Loading States
- Skeleton screens for content
- Spinners for actions
- Progress bars for uploads
- Smooth transitions

## Dark Mode Considerations

Current implementation uses dark theme by default:
- Background: Very dark blue (#0a0f19)
- Text: Light gray (#f3f4f6)
- Accents: Bright cyan and purple
- Glass effects with low opacity

## Future Enhancements

### Planned Improvements
1. Light mode support with theme toggle
2. Custom theme builder
3. Animation preferences (reduced motion)
4. Font size preferences
5. High contrast mode
6. RTL language support
7. Advanced keyboard shortcuts
8. Voice command integration
9. Gesture controls for mobile
10. Haptic feedback on mobile

### Component Library
Consider extracting common components:
- Button variants
- Input fields
- Cards
- Modals
- Tooltips
- Dropdowns
- Tabs
- Accordions

## Testing Guidelines

### Visual Testing
- Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- Test on multiple devices (mobile, tablet, desktop)
- Test with different screen sizes
- Test with browser zoom (100%, 150%, 200%)

### Accessibility Testing
- Use screen reader (NVDA, JAWS, VoiceOver)
- Test keyboard-only navigation
- Use accessibility audit tools (axe, Lighthouse)
- Test with high contrast mode

### Performance Testing
- Lighthouse performance score > 90
- First Contentful Paint < 1.5s
- Time to Interactive < 3.5s
- Cumulative Layout Shift < 0.1

## Resources

### Tools
- Figma/Sketch for design mockups
- Chrome DevTools for debugging
- Lighthouse for audits
- axe DevTools for accessibility
- React DevTools for performance

### References
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Material Design](https://material.io/design)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Inclusive Components](https://inclusive-components.design/)

---

Last Updated: April 4, 2026
Version: 2.0
