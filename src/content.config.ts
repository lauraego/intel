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
    // Article redesign (Laura approved 2026-11-11)
    heroImage: z.string(),            // site path, 1600x900 WebP, e.g. /blog/<slug>/hero.webp
    heroAlt: z.string(),
    kicker: z.string().optional(),    // hero eyebrow, e.g. "Patterns"
    titleEm: z.string().optional(),   // part of the title drawn in gold
    hook: z.string(),                 // one italic line under the byline
    forWho: z.string(),               // "who this is for" line
    answer: z.array(z.string()).min(1), // "The short answer" card paragraphs
  }),
});

export const collections = { blog };
