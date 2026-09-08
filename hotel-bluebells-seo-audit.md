# SEO Audit — Hotel Bluebells (Pre-Launch Site)

**Site:** `hotel-bluebells-site-theme-changed` (local dev, not yet deployed)
**Pages reviewed:** 14 (index, about, contact, faq, gallery, neighbourhood, offers, privacy-policy, rooms, room-double, room-family, room-quad, room-single, room-triple)
**Date:** 7 September 2026

This is a **technical + on-page audit**, since the site isn't live yet — there's no domain, no rankings, no backlinks, and no traffic to analyze. Keyword research and competitor comparison will be far more useful once you've picked a domain and gone live; happy to run those at that point.

## Overall Score: 37 / 100 — Needs work before launch

| Category | Score | Weight |
|---|---|---|
| Crawlability & Indexability | 6 / 20 | robots.txt, sitemap, canonical tags |
| On-Page Meta (titles/descriptions/H1) | 19 / 20 | Strong |
| Content & Accessibility (alt text, headings) | 8 / 15 | Weak |
| Structured Data & Social Tags | 1 / 15 | Almost entirely missing |
| Performance / Core Web Vitals readiness | 3 / 30 | Critical — biggest issue on the site |

**Bottom line:** whoever wrote your titles and meta descriptions did a genuinely good job — they're unique, on-topic, and location-aware across all 14 pages. But the site is missing the technical scaffolding search engines rely on (robots.txt, sitemap, canonical tags, structured data), and it's carrying **175 MB of images** with no compression, no lazy-loading, and no dimensions set — which will tank your Core Web Vitals and, with it, your rankings, the moment this goes live.

---

## Critical Issues

| Page | Issue | Severity | Fix |
|---|---|---|---|
| Site-wide | No `robots.txt` file | Critical | Add one at the site root; at minimum allow all and reference the sitemap |
| Site-wide | No `sitemap.xml` | Critical | Generate one listing all 14 pages; submit to Google Search Console after launch |
| Site-wide (13 of 14 pages) | No canonical tag | High | Add `<link rel="canonical">` to every page |
| `neighbourhood.html` | Canonical tag points to `https://YOURDOMAIN/neighbourhood.html` — a literal placeholder | Critical | This is a leftover template value. Replace with the real domain before launch or it will actively confuse crawlers |
| Site-wide | 175 MB of images across 52 files; 50 files over 1 MB, 3 files over **20 MB each** (`facade.jpg` 22.3 MB, `hero _ neighbourhood.jpg` 22.5 MB, `Hero image.jpg` 20.2 MB) | Critical | Compress and convert to WebP/AVIF. A hero image should be 100–300 KB, not 20 MB. This alone will likely fail Google's Core Web Vitals (LCP) on every page |
| Site-wide | No image `width`/`height` attributes anywhere | High | Set explicit dimensions (or `aspect-ratio` in CSS) to prevent layout shift (CLS) |
| Site-wide | No `loading="lazy"` on any image | High | Add lazy-loading to below-the-fold images (galleries, room pages especially — one page has 15 images) |
| Site-wide | Zero Open Graph tags, zero Twitter Card tags | High | Add `og:title`, `og:description`, `og:image`, `og:type` — without these, links shared on Facebook/WhatsApp/LinkedIn/X show no preview card |
| Site-wide (13 of 14 pages) | No structured data (JSON-LD) | High | A hotel site should have `Hotel`/`LodgingBusiness` schema site-wide, plus `Room` schema on room pages. Only `neighbourhood.html` has any JSON-LD |
| ~45 images site-wide | Missing or empty `alt` attributes (3–6 per page, every page affected) | High | Every image needs descriptive alt text — accessibility requirement and a ranking/image-search signal |
| `index.html` | Two `<h1>` tags on the homepage ("Welcome to Bluebells" and "A Victorian Townhouse...") | Medium | Keep one H1 per page; demote the second to `<h2>` |
| `neighbourhood.html` | Meta description is 218 characters | Low | Trim to ~155 characters or Google will truncate it in search results |
| Site-wide | Duplicate images (e.g. `quad room.png`, `quad room(1).png`, `quad room(2).png`; also a separate `/images/rooms/` folder duplicating 5 files already in `/images/`) | Low | Clean up — reduces confusion and repo/deploy size, no direct ranking harm but worth tidying |
| Project root | A 45 MB video file (`20260907-2114-20.5480656.mp4`) sits in the site root and isn't referenced by any page | Low | Looks like a stray screen recording — remove before deploying, or move outside the web root |

---

## Technical SEO Checklist

| Check | Status | Details |
|---|---|---|
| Title tags | ✅ Pass | Unique on all 14 pages, 44–64 characters, location-aware |
| Meta descriptions | ✅ Pass | Unique on 14/14 pages, mostly 100–130 chars (one at 218 — trim it) |
| `html lang` attribute | ✅ Pass | `lang="en"` set on every page |
| Viewport meta (mobile) | ✅ Pass | Present and correct on all pages |
| Favicon | ✅ Pass | Inline SVG favicon, lightweight |
| H1 usage | ⚠️ Warning | 1 per page except homepage (2) |
| Meta robots (accidental noindex) | ✅ Pass | None found — nothing is blocking indexing |
| Canonical tags | ❌ Fail | 1 of 14 pages has one, and it's a broken placeholder |
| `robots.txt` | ❌ Fail | Not present |
| `sitemap.xml` | ❌ Fail | Not present |
| Image alt text | ❌ Fail | Missing/empty on every page |
| Open Graph / Twitter Card tags | ❌ Fail | Absent site-wide |
| JSON-LD structured data | ❌ Fail | Present on 1 of 14 pages only |
| Image optimization | ❌ Fail | 175 MB total, unoptimized PNG/JPG |
| Lazy loading | ❌ Fail | Not used anywhere |
| Image dimensions set (CLS) | ❌ Fail | Not used anywhere |
| HTTPS | — N/A | Local dev site; must be enforced at launch |

---

## Prioritized Action Plan

**Quick wins (do this week, high impact, low effort):**
1. Replace the `https://YOURDOMAIN` placeholder in `neighbourhood.html`'s canonical tag, and add correct canonical tags to the other 13 pages.
2. Create a `robots.txt` and a `sitemap.xml`.
3. Fix the homepage's double-H1.
4. Add missing/empty `alt` text to all images (~45 across the site).
5. Trim the `neighbourhood.html` meta description to under 160 characters.
6. Delete or relocate the stray 45 MB video file and the duplicate room images.

**Strategic investments (before or shortly after launch):**
1. **Compress and convert every image to WebP/AVIF** and cap dimensions to what's actually displayed. This is the single highest-impact fix on the site — a 175 MB image budget is roughly 50–100x what a fast-loading hotel site should carry.
2. Add `width`/`height` (or CSS `aspect-ratio`) to every `<img>` and add `loading="lazy"` to below-the-fold images.
3. Add Open Graph and Twitter Card tags site-wide so links shared on social/WhatsApp render properly.
4. Add `Hotel`/`LodgingBusiness` JSON-LD schema site-wide (address, price range, amenities), plus `Room` schema on the five room pages — this is what powers rich results for hotel listings.
5. Once the site has a real domain, run keyword research and a competitor comparison (Portobello Road / Notting Hill boutique hotels) to shape title tags and content strategy further.

---

*This audit covers technical and on-page SEO only, since the site isn't live. Once you have a domain and go live, I can also run keyword research, a content gap analysis against competitor hotels in the area, and re-check Core Web Vitals with real load data.*
