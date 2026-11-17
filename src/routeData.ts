// Keeps the sidebar small: every phase is listed, but only the current phase shows its lessons.
// (Rendering all 542 lessons on every page made each page ~3x larger.)
// Prev/next links are computed by Starlight before this runs, so they still cross phases.
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

type Entry = { type: 'link' | 'group'; label: string; href?: string; isCurrent?: boolean; entries?: Entry[]; [k: string]: unknown };

const hasCurrent = (e: Entry): boolean => (e.type === 'link' ? !!e.isCurrent : (e.entries ?? []).some(hasCurrent));
const firstLink = (e: Entry): Entry | undefined => (e.type === 'link' ? e : (e.entries ?? []).map(firstLink).find(Boolean));

export const onRequest = defineRouteMiddleware((context) => {
  const route = context.locals.starlightRoute;
  route.sidebar = (route.sidebar as Entry[]).map((entry) => {
    if (entry.type !== 'group') return entry;
    if (hasCurrent(entry)) return { ...entry, collapsed: false };
    const first = firstLink(entry);
    return { type: 'link', label: entry.label, href: first?.href ?? '#', isCurrent: false, badge: undefined, attrs: {} };
  }) as typeof route.sidebar;
});
