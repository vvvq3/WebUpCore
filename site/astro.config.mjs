// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://up-core.ru',
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'always' },
  compressHTML: true,
  integrations: [
    sitemap({
      i18n: { defaultLocale: 'ru', locales: { ru: 'ru-RU', en: 'en-US' } },
      filter: (page) => !page.includes('/404'),
    }),
  ],
  // приведение типа: у @tailwindcss/vite и Astro разные версии типов Vite (на сборку не влияет)
  vite: { plugins: [/** @type {any} */ (tailwindcss())] },
});
