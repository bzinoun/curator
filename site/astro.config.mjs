import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://bzinoun.github.io',
  base: '/curator',
  markdown: {
    shikiConfig: { theme: 'github-dark-dimmed' },
  },
});
