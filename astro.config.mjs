// @ts-check
import fs from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import remarkLesson from './src/plugins/remark-lesson.mjs';

const phases = JSON.parse(fs.readFileSync(new URL('./src/data/phases.json', import.meta.url), 'utf8'));
const docsDir = new URL('./src/content/docs/en/', import.meta.url);

// One sidebar group per phase that has at least one imported lesson.
const phaseGroups = phases
  .filter((p) => fs.existsSync(new URL(`${p.id}/`, docsDir)))
  .map((p) => {
    const num = p.id.slice(0, 2);
    return {
      label: `Phase ${num} · ${p.en}`,
      translations: { th: `Phase ${num} · ${p.th}` },
      items: [{ autogenerate: { directory: p.id } }],
    };
  });

export default defineConfig({
  // GitHub Pages / sub-path hosting: set SITE_BASE=/repo-name/ when building.
  base: process.env.SITE_BASE || '/',
  trailingSlash: 'always',
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath, remarkLesson],
    }),
  },
  integrations: [
    starlight({
      title: 'AI-Learning',
      description: 'เรียน AI ด้วยการลงมือสร้างเอง · Learn AI engineering by building it',
      defaultLocale: 'en',
      locales: {
        en: { label: 'English', lang: 'en' },
        th: { label: 'ไทย', lang: 'th' },
      },
      logo: { src: './src/assets/logo.svg', alt: 'AI-Learning' },
      favicon: '/favicon.svg',
      head: [
        // Remember the reader's language so the site root opens in it next time.
        {
          tag: 'script',
          content: "try{localStorage.setItem('ail-lang',document.documentElement.lang.slice(0,2))}catch(e){}",
        },
      ],
      customCss: [
        '@fontsource/ibm-plex-sans-thai/400.css',
        '@fontsource/ibm-plex-sans-thai/500.css',
        '@fontsource/ibm-plex-sans-thai/600.css',
        '@fontsource/ibm-plex-sans-thai/700.css',
        '@fontsource/jetbrains-mono/400.css',
        '@fontsource/jetbrains-mono/500.css',
        'katex/dist/katex.min.css',
        './src/styles/theme.css',
        './src/styles/lesson.css',
      ],
      components: {
        MarkdownContent: './src/components/MarkdownContent.astro',
      },
      expressiveCode: {
        themes: ['one-dark-pro'],
        styleOverrides: {
          borderRadius: '12px',
          codeFontFamily: "'JetBrains Mono', ui-monospace, monospace",
          codeFontSize: '0.875rem',
          codeLineHeight: '1.7',
        },
      },
      sidebar: phaseGroups,
      lastUpdated: false,
      credits: false,
    }),
  ],
});
