// One lookup table of all docs entries, built once per build instead of once per page.
import { getCollection, type CollectionEntry } from 'astro:content';

let cache: Promise<Map<string, CollectionEntry<'docs'>>> | null = null;

export function docsIndex() {
  cache ||= getCollection('docs').then((entries) => new Map(entries.map((e) => [e.id, e])));
  return cache;
}
