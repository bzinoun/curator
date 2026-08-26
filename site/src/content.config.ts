import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    lang: z.enum(['fr', 'en', 'ary']),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../published' }),
  schema: z.object({
    title: z.string(),
    format: z.enum(['linkedin', 'tweet']),
    lang: z.enum(['fr', 'en', 'ary']),
    status: z.string(),
    date: z.coerce.date(),
    link: z.string().optional(),
    visual: z.string().optional(),
    nuggets: z.array(z.string()).default([]),
  }),
});

export const collections = { articles, posts };
