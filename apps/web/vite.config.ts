import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import dns from 'node:dns'

// Force Node.js to use IPv4 first for DNS resolution
// This prevents the 5-second delay when resolving .local domains
dns.setDefaultResultOrder('ipv4first')

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0', // Allow external connections
    allowedHosts: [
      'localhost',
      'web.haven.local',
      'app.haven.local',
      'haven.local',
    ],
    proxy: {
      '/api': {
        // Use 127.0.0.1 directly to avoid DNS resolution delays
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        headers: {
          // Preserve the original host header for the backend
          'X-Forwarded-Host': 'api.haven.local',
        },
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // Ensure the backend receives the correct host
            proxyReq.setHeader('Host', 'api.haven.local');
          });
        },
      },
      '/graphql': {
        // Use 127.0.0.1 directly to avoid DNS resolution delays
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        headers: {
          // Preserve the original host header for the backend
          'X-Forwarded-Host': 'api.haven.local',
        },
        configure: (proxy, _options) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            // Ensure the backend receives the correct host
            proxyReq.setHeader('Host', 'api.haven.local');
          });
        },
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})