# Haven Web Client

A React + TypeScript web client for the Haven API, built with Vite and Tailwind CSS.

## Features

- 🚀 **React 18**: Modern React with hooks and functional components
- 🔧 **TypeScript**: Full type safety
- ⚡ **Vite**: Lightning-fast development and builds
- 🎨 **Tailwind CSS**: Utility-first styling
- 🔄 **React Query**: Powerful data fetching and caching
- 🧭 **React Router**: Client-side routing
- ✅ **ESLint**: Code linting
- 💅 **Prettier**: Code formatting

## Quick Start

```bash
# From the repository root:
cd apps/web
npm install
npm run dev
```

The development server will start at http://web.haven.local with API proxy to http://api.haven.local.

## Available Scripts

```bash
npm run dev         # Start development server
npm run build       # Build for production
npm run preview     # Preview production build
npm run lint        # Run ESLint
npm run format      # Format code with Prettier
npm run type-check  # TypeScript type checking
```

## Project Structure

```
apps/web/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── hooks/         # Custom React hooks
│   ├── types/         # TypeScript type definitions
│   ├── utils/         # Utility functions
│   ├── App.tsx        # Main application component
│   ├── main.tsx       # Application entry point
│   └── index.css      # Global styles
├── public/            # Static assets
├── index.html         # HTML template
└── vite.config.ts     # Vite configuration
```

## Development

### API Integration

The development server proxies API requests to the Haven API server:
- `/api/*` → `http://api.haven.local/api/*`
- `/graphql` → `http://api.haven.local/graphql`

Make sure the API server is running on port 8080 before starting the web client.

### Styling

This project uses Tailwind CSS for styling. The configuration is in `tailwind.config.js`.

### State Management

React Query is used for server state management, providing caching, background updates, and optimistic updates.

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.