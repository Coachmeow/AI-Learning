import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader, i18nLoader } from '@astrojs/starlight/loaders';
import { docsSchema, i18nSchema } from '@astrojs/starlight/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        // Upstream lesson this page comes from, e.g. "phases/01-math-foundations/08-optimization".
        upstream_path: z.string().optional(),
        upstream_commit: z.string().optional(),
        // sha256 of the upstream docs/en.md this page was imported or translated from.
        source_hash: z.string().optional(),
      }),
    }),
  }),
  i18n: defineCollection({ loader: i18nLoader(), schema: i18nSchema() }),
};
