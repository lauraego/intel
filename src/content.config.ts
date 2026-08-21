import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    cluster: z.enum(['scroll', 'ai-infrastructure']),
    tags: z.array(z.string()).default([]),
    faqs: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
    cta: z.enum(['scroll', 'operator']).default('scroll'),
  }),
});

export const collections = { blog };
