import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import { djangoVitePlugin } from 'django-vite-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    djangoVitePlugin({
      input: [
        'static/css/style.css',
        'static/js/dj.js',
      ],
      root: "..",
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: '../vite_build',
  }
})
