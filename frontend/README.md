# 🎨 Bibliotheca AI - Frontend

Next.js frontend with a beautiful library-themed interface for the Bibliotheca AI document intelligence system.

## 📋 Overview

A modern, responsive web application featuring a vintage library aesthetic with parchment backgrounds, leather textures, and gold accents. Built with Next.js 16, TypeScript, and Tailwind CSS.

## ✨ Features

### 🎨 Library Theme
- **Parchment Background**: Warm, aged paper aesthetic
- **Leather Textures**: Rich brown buttons and cards
- **Gold Accents**: Elegant highlights and badges
- **Serif Typography**: Georgia font for classic book feel
- **Custom Scrollbars**: Leather-textured scroll elements

### 📱 Components

#### Chat Interface
- Real-time conversation with AI agent
- Markdown rendering for formatted responses
- Message history with user/assistant distinction
- Auto-scroll to latest messages
- Loading states and error handling

#### Upload Panel
- Drag & drop file upload
- Support for PDF, DOCX, TXT
- Upload progress indication
- Success/error feedback
- Auto-refresh document list

#### Documents Panel
- Hierarchical document view
- Expandable chunks with metadata
- Embedding dimension display
- Individual document deletion
- Full-text search within chunks

#### Stats Panel
- Database type indicator (ChromaDB/Pinecone)
- Document count and collection info
- Embedding model display
- Agent configuration (model, temperature, top-k)
- Storage location (local/cloud)
- Manual refresh with animation

## 🚀 Setup

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# or
yarn install
```

### Configuration

Create `.env.local` in the frontend directory:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev

# or
yarn dev
```

Open http://localhost:3000

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 🎨 Theme Customization

### Color Palette

The library theme uses CSS custom properties defined in `src/app/globals.css`:

```css
:root {
  --color-parchment: #f8f6f0;      /* Background */
  --color-aged-paper: #e8e4d8;     /* Cards */
  --color-leather: #8b4513;        /* Buttons */
  --color-dark-wood: #3e2723;      /* Text */
  --color-gold: #d4af37;           /* Accents */
  --color-burgundy: #800020;       /* Highlights */
  --color-forest: #2d5016;         /* Success */
  --color-ink: #1a1a1a;           /* Primary text */
}
```

### Custom Classes

- `.library-card` - Parchment-style card
- `.library-card-dark` - Dark wood card with gold border
- `.btn-leather` - Leather-textured button
- `.gold-accent` - Gold text with shadow
- `.book-spine` - Book spine effect
- `.ornament` - Decorative elements (❦)

### Modifying the Theme

To change colors, edit `src/app/globals.css`:

```css
/* Example: Change to blue theme */
:root {
  --color-leather: #2c5282;  /* Blue instead of brown */
  --color-gold: #4299e1;     /* Light blue instead of gold */
}
```

## 📦 Dependencies

### Core
- `next` (16.1.6) - React framework
- `react` (19.2.3) - UI library
- `react-dom` (19.2.3) - React DOM renderer
- `typescript` (^5) - Type safety

### UI & Styling
- `tailwindcss` (^4) - Utility-first CSS
- `@tailwindcss/postcss` (^4) - PostCSS plugin
- `lucide-react` (^0.575.0) - Icon library

### Utilities
- `axios` (^1.13.5) - HTTP client
- `react-markdown` (^10.1.0) - Markdown rendering

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── globals.css        # Global styles & theme
│   │   └── favicon.ico        # Favicon
│   ├── components/            # React components
│   │   ├── ChatInterface.tsx  # Chat UI
│   │   ├── UploadPanel.tsx    # File upload
│   │   ├── DocumentsPanel.tsx # Document browser
│   │   └── StatsPanel.tsx     # System stats
│   ├── lib/                   # Utilities
│   │   └── api.ts            # API client
│   └── types/                 # TypeScript types
│       └── index.ts          # Type definitions
├── public/                    # Static assets
├── .env.local                # Environment variables (gitignored)
├── next.config.ts            # Next.js configuration
├── tailwind.config.ts        # Tailwind configuration
├── tsconfig.json             # TypeScript configuration
├── package.json              # Dependencies
└── README.md                 # This file
```

## 🔧 API Client

The API client (`src/lib/api.ts`) provides typed methods for backend communication:

```typescript
import { apiClient } from '@/lib/api';

// Query the RAG system
const response = await apiClient.query({
  question: "What is machine learning?",
  conversation_id: "session-123"
});

// Upload document
const result = await apiClient.ingestDocument(file);

// Get system stats
const stats = await apiClient.getStats();

// Get all documents
const docs = await apiClient.getAllDocuments();

// Delete document
await apiClient.deleteDocument(source);
```

## 🎯 Component Usage

### ChatInterface

```tsx
import ChatInterface from '@/components/ChatInterface';

<ChatInterface />
```

Features:
- Maintains conversation state
- Handles message sending
- Renders markdown responses
- Auto-scrolls to new messages

### UploadPanel

```tsx
import UploadPanel from '@/components/UploadPanel';

<UploadPanel onUploadSuccess={() => console.log('Uploaded!')} />
```

Props:
- `onUploadSuccess?: () => void` - Callback after successful upload

### DocumentsPanel

```tsx
import DocumentsPanel from '@/components/DocumentsPanel';

const ref = useRef<DocumentsPanelRef>(null);

<DocumentsPanel ref={ref} />

// Manually refresh
ref.current?.refresh();
```

Methods:
- `refresh()` - Reload documents from API

### StatsPanel

```tsx
import StatsPanel from '@/components/StatsPanel';

<StatsPanel />
```

Features:
- Auto-refreshes every 60 seconds
- Manual refresh button
- Shows database type, model, and config

## 🎨 Styling Guide

### Using Library Theme Classes

```tsx
// Parchment card
<div className="library-card rounded-xl p-6">
  Content
</div>

// Dark wood card
<div className="library-card-dark rounded-xl p-6">
  Content
</div>

// Leather button
<button className="btn-leather px-4 py-2 rounded-lg">
  Click Me
</button>

// Gold accent text
<span className="gold-accent text-xl">
  Important Text
</span>
```

### Responsive Design

```tsx
// Mobile-first approach
<div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
  <div className="lg:col-span-3">Sidebar</div>
  <div className="lg:col-span-9">Main</div>
</div>
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
PORT=3001 npm run dev
```

### API Connection Issues
1. Check backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check browser console for CORS errors

### Styling Not Applied
1. Restart dev server after Tailwind config changes
2. Clear `.next` cache: `rm -rf .next`
3. Rebuild: `npm run build`

### TypeScript Errors
```bash
# Check types
npm run type-check

# or
tsc --noEmit
```

## 📱 Responsive Breakpoints

Tailwind breakpoints used:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

## ♿ Accessibility

- Semantic HTML elements
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus indicators
- Alt text for icons (via Lucide)

## 🚀 Performance

### Optimization Tips
1. Use Next.js Image component for images
2. Lazy load heavy components
3. Implement virtual scrolling for large lists
4. Debounce search inputs
5. Use React.memo for expensive renders

### Bundle Analysis
```bash
# Analyze bundle size
npm run build
npm run analyze
```

## 🔄 Updates

```bash
# Update all dependencies
npm update

# Update specific package
npm install next@latest

# Check for outdated packages
npm outdated
```

## 📊 Build Output

After `npm run build`:
- Static pages in `.next/static`
- Server components in `.next/server`
- Optimized for production deployment

## 🌐 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables
Set in deployment platform:
- `NEXT_PUBLIC_API_URL` - Backend API URL

## 📧 Support

For frontend-specific issues:
1. Check browser console for errors
2. Verify API connectivity
3. Check component props and types

---

**Part of Bibliotheca AI - Intelligent Document Library**
