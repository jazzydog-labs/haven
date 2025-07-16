import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

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
        target: 'http://api.haven.local:8080',
        changeOrigin: true,
      },
      '/graphql': {
        target: 'http://api.haven.local:8080',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})