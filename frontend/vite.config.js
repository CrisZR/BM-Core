import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  // base: "/static/",
  build: {
    outDir: 'dist', // por defecto, pero puede cambiar si quieres
  },
  plugins: [react()],
})
