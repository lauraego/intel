import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://intel.viralgrowthmedia.ai',
  integrations: [sitemap()],
  trailingSlash: 'never',
  build: { format: 'file' },
  redirects: {
    '/blog/business-runs-on-ai-agents': 'https://viralgrowthmedia.io/business-runs-on-ai-agents/',
    '/blog/automate-instagram-dm-responses': 'https://viralgrowthmedia.io/automate-instagram-dm-responses/',
    '/blog/what-is-an-ai-revenue-system': 'https://viralgrowthmedia.io/what-is-an-ai-revenue-system/',
    '/blog/ai-operated-business-field-guide': 'https://viralgrowthmedia.io/ai-operated-business-field-guide/',
  },
});
