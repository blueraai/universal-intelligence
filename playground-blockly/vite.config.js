import { defineConfig } from 'vite'
import path from 'path'

export default defineConfig({
  root: '.',
  base: '/playground-blockly/',
  server: {
    port: 8001,
    open: false,
    host: true,
    allowedHosts: ['dev.chrisbradd.io', 'localhost', '127.0.0.1'],
    fs: {
      // Allow serving files from the parent directory
      allow: ['..']
    }
  },
  resolve: {
    alias: {
      // Alias universalintelligence to the built files
      'universalintelligence': path.resolve(__dirname, '../distweb/index.js')
    }
  }
})