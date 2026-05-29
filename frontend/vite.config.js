import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: null,   // prevent the no-op fetch handler warning
      workbox: { globPatterns: [] },
    }),
  ],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false
      },
      '/chat': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false
      },
      '/chat_stream': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  },
  optimizeDeps: {
    include: ['framer-motion', 'axios', 'lucide-react']
  }
})
