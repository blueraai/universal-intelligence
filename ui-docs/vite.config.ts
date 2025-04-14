import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173, // optional, in case you're routing via DNS or proxy
    allowedHosts: ['dev.chrisbradd.io'], // <== allow your Ngrok host
  },
})