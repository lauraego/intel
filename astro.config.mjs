import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://intel.viralgrowthmedia.ai',
  integrations: [sitemap()],
  trailingSlash: 'never',
  build: { format: 'file' },
});
