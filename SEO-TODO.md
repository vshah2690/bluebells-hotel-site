# SEO TODO - Hotel Bluebells

Branch: `seo-fixes`. Everything below needs your input or happens after launch.
Line numbers are for the `seo-fixes` branch as committed.

## 1. Needs owner decision

### 1.1 "18th-century Victorian townhouse" (self-contradictory - NOT changed)
Victorian = 1837-1901, so "18th-century Victorian" cannot both be true. Confirm the real period,
then update every place below. Wording was deliberately left as it was.

- **Meta description + og:description** (change both together): `index.html:7`, `index.html:17`, `about.html:7`, `about.html:17`
- **JSON-LD** (copies of the wording - update too, or Google sees the old text): `index.html:638`, `faq.html:692`
- **Visible page text:** `about.html:811` (eveal"> <p class="eyebrow">Since the 18th Century</p> <svg class="scrollw...); `about.html:814` (ells has stood on Pembridge Square since the 18th century, one of the handsome V...); `about.html:832` (le="--stagger:0"> <span class="year">18th Century</span> <p>The townhouse...); `faq.html:1006` (<div class="faq-answer">The building is an 18th-century townhouse without a lift...)
- **Footer blurb on all 14 pages** ("An 18th-century Victorian townhouse turned boutique hotel..."): `index.html:1407`, `about.html:881`, `contact.html:970`, `deluxe-double-room.html:1001`, `executive-triple-room.html:1009`, `family-junior-suite.html:1009`, `family-suite.html:1011`, `faq.html:1071`, `gallery.html:888`, `neighbourhood.html:1032`, `offers.html:871`, `privacy-policy.html:926`, `rooms.html:929`, `standard-single-room.html:997`
- **Inside HTML comments only (not shown):** `index.html:942`, `index.html:997`

Related: room-page meta descriptions and room copy still say "Victorian townhouse" / "high Victorian ceilings"
(existing wording, kept). The image alt text I wrote is period-neutral on purpose.

### 1.2 Booking URL (SiteMinder) - 66 placeholder links still `href="#"`
No URL exists yet, so these were left alone. When you have the SiteMinder URL, replace them all
(external URL -> add `target="_blank" rel="noopener"`). Every page has the nav button + mobile-menu
button + footer "Book Now" link; some have extra buttons.

| Page | Count | Where (line - label) |
|---|---|---|
| `index.html` | 5 | L869 Book Now; L892 Book Now; L945 Check Availability; L1426 Book Now; L1445 Terms & Conditions |
| `about.html` | 4 | L758 Book Now; L781 Book Now; L900 Book Now; L919 Terms & Conditions |
| `contact.html` | 5 | L835 Book Now; L858 Book Now; L905 Hotel Bluebells on Facebook; L989 Book Now; L1008 Terms & Conditions |
| `deluxe-double-room.html` | 5 | L886 Book Now; L909 Book Now; L963 Book Now; L1020 Book Now; L1039 Terms & Conditions |
| `executive-triple-room.html` | 5 | L894 Book Now; L917 Book Now; L971 Book Now; L1028 Book Now; L1047 Terms & Conditions |
| `family-junior-suite.html` | 5 | L894 Book Now; L917 Book Now; L971 Book Now; L1028 Book Now; L1047 Terms & Conditions |
| `family-suite.html` | 5 | L897 Book Now; L920 Book Now; L973 Book Now; L1030 Book Now; L1049 Terms & Conditions |
| `faq.html` | 4 | L927 Book Now; L950 Book Now; L1090 Book Now; L1109 Terms & Conditions |
| `gallery.html` | 5 | L758 Book Now; L781 Book Now; L798 Book Now; L907 Book Now; L926 Terms & Conditions |
| `neighbourhood.html` | 4 | L780 Book Now; L803 Book Now; L1051 Book Now; L1070 Terms & Conditions |
| `offers.html` | 5 | L758 Book Now; L781 Book Now; L851 Buy A Voucher; L890 Book Now; L909 Terms & Conditions |
| `privacy-policy.html` | 4 | L773 Book Now; L796 Book Now; L945 Book Now; L964 Terms & Conditions |
| `rooms.html` | 5 | L763 Book Now; L786 Book Now; L803 Book Now; L948 Book Now; L967 Terms & Conditions |
| `standard-single-room.html` | 5 | L882 Book Now; L905 Book Now; L959 Book Now; L1016 Book Now; L1035 Terms & Conditions |

Notes on the above:
- `offers.html` "Buy A Voucher" needs a voucher / booking-engine URL.
- `index.html` "Check Availability" is the homepage hero CTA.
- Every "Terms & Conditions" footer link is a placeholder: no terms page exists. Publish one (or drop the link).
- `contact.html` Facebook icon: I have no Facebook URL. (Instagram is wired to your supplied profile.)
- `python scripts/seo_check.py --strict` treats these as failures. Run it before launch to prove none remain.

### 1.3 Facts I did not invent (add when known)
- **Coordinates:** the map embed on `contact.html` searches by address, so it has no lat/long. Add `geo`
  (`GeoCoordinates`) to the `Hotel` JSON-LD on `index.html` and `contact.html`.
- **Star rating:** none supplied, so no `starRating`. (One guest review on the homepage says "3 star"; that
  is not an official rating and was not used.)
- **Facebook / other social URLs** for `sameAs` (only Instagram is in the schema, as the clean profile URL
  `https://www.instagram.com/hotel_bluebells/` - the `utm_source` share-sheet parameter was dropped).
- **No `aggregateRating` / `review` markup**, as instructed. The static Google-Business-profile reviews on the
  homepage are plain text; keep them accurate and current.
- **Hotel address in schema** is `14 Pembridge Square, London W2 4EH, GB`. "Notting Hill Gate" (used in the
  page text) is not in the schema address; keep name/address/phone identical to your Google Business Profile.

### 1.4 Site content that contradicts itself (left as is; schema avoids the disputed claims)
- **Breakfast:** homepage says "Included if booked direct"; FAQ and 4 room pages say included with every rate;
  `standard-single-room.html` does not list breakfast at all. Breakfast is therefore *not* in the Hotel schema.
- **Mini fridge** appears on the homepage amenity cards but on no room page, so it is not in the schema.

### 1.5 Placeholder / weak content
- `faq.html` hero is an external grey placeholder (`placehold.co ... "FAQ HERO 1920x900"`). Replace with a real photo
  (I gave it `alt=""` and did not use it for `og:image`).
- Redirect rows marked UNCERTAIN in `redirects-for-launch/redirects.csv` (reservation, terms, guest-book, careers,
  `?roomId=` values, `family_room.html`). Decide the targets; each row's note explains the options.
- Titles over 60 characters (may truncate): `executive-triple-room` (62), `standard-single-room` (61),
  `neighbourhood` (64). Meta descriptions too long: `neighbourhood` (218), `rooms` (172). Short but acceptable:
  `gallery` (106), `offers` (110), `privacy-policy` (115). You asked me to change only the FAQ title and room
  descriptions, so these were left.

## 2. Decisions I made that you may want to revisit
- Homepage links use `/` and `/#newsletterForm` exactly as requested. **Side effect on the github.io review copy:**
  "Home"/logo links go to `vshah2690.github.io/` (outside the project folder). Production is unaffected. If it bothers you
  during review, `./` works on both.
- Breadcrumbs on room pages are Home > Rooms > Room (not just Home > Room) to match the real hierarchy.
- The lightbox `<img src="">` (present on every page; it is the lightbox overlay, not a footer image) was kept - the
  script needs it - and given a 1x1 transparent GIF.
- Footer column labels were `<h5>`; they are now styled `<p>` (same look, verified by screenshots) so headings do not skip levels.
- `og:image` for `contact.html` and `offers.html` are 2 MB PNGs (WebP is not accepted by all social scrapers).
  Create 1200x630 JPGs under ~300 KB for those two.
- `sitemap.xml` `<lastmod>` values come from `git log` at the time it was generated. Regenerate at launch if content changed.
- Room-page JSON-LD points to the Hotel by `@id`. Google does not follow `@id` across pages; harmless, but you may
  prefer to embed a small Hotel object on each room page later.

## 3. Launch checklist (in order)
1. `git checkout main`, merge `seo-fixes` after your review.
2. Fill in the booking URLs / terms page / coordinates above (or accept them as post-launch).
3. **Run `python scripts/go-live.py`** - removes the staging `noindex` block from every page and prints how many
   pages changed (expect 14). View source on 2-3 pages: no `noindex` anywhere.
4. `python scripts/seo_check.py --strict` - must print `OK ... 0 failures`.
5. **Back up the old site first** (cPanel > Backup). Upload the new site to `public_html/`. **Upload only the website**: do not upload `scripts/`, `redirects-for-launch/`,
   `SEO-TODO.md`, `hotel-bluebells-seo-audit.md`, `.claude/` or `.git/` (they would be publicly downloadable).
6. Copy `redirects-for-launch/.htaccess` to `public_html/.htaccess` (merge with any cPanel PHP-handler lines).
   The redirect rules fire before any old `.php` file runs; delete the old PHP files only after the redirects are tested.
7. Confirm HTTPS works (cPanel AutoSSL) and that `http://` and non-`www` redirect to `https://www.hotelbluebells.com/`
   in ONE hop: `curl -sI http://hotelbluebells.com/` .
8. Test at least 10 old URLs return **301** to the right page, e.g. `/index.php`,
   `/bluebells-hotel-london-room-rates-facilities.php?roomId=2`, `/bluebells-hotel-notting-hill-gate-contact.php`,
   `/bluebells-hotel-nottinghill-gate-london-attraction.php`, `/bluebells-hotel-hyde-park-photo-gallery.php`,
   `/bluebells-hotel-hyde-park-group-reservation.php`, `/family_room.html`, `/double_room.html`, `/index.html`,
   `https://hotelbluebells.com/faq.html`.
9. Google Search Console: add the `https://www.hotelbluebells.com/` property, submit `https://www.hotelbluebells.com/sitemap.xml`,
   then use URL Inspection on the homepage and "Request indexing".
10. Run two pages (homepage + `faq.html`) through Google's Rich Results Test (`Hotel`, `FAQPage`, breadcrumbs).
11. Google Business Profile: the same **name, address and phone** as the site: Hotel Bluebells, 14 Pembridge Square,
    London W2 4EH, +44 20 7727 6666. Add the website URL `https://www.hotelbluebells.com/`.

## 4. Do after launch
- **Old URLs:** export every URL Google has indexed for the old site (Search Console > Pages, or crawl the old site) and add any not in
  `redirects.csv` before you switch DNS. Old URLs that 404 are the biggest ranking risk in this migration.
- Watch Search Console (Pages, Sitemaps, Enhancements, Core Web Vitals) for the first 2-4 weeks; expect a dip while Google re-crawls.
- Run PageSpeed Insights on the homepage, a room page and the gallery; check LCP (hero) and CLS.
- Add `geo`, star rating (only if official) and Facebook `sameAs` once known; re-test in the Rich Results Test.
- Replace the `href="#"` placeholders with SiteMinder links (see 1.2) and re-run `seo_check.py --strict`.
- Tidy `images/`: 105 files, only ~50 used; several duplicates (`images/rooms/`, copies at the root). Originals were kept
  on purpose - delete unused ones once you are sure.
- Reviews and Google Business Profile: keep collecting real Google reviews - they, not on-page markup, drive review stars in search.
- Consider one landing page each for high-intent searches (e.g. "hotel near Portobello Road", "family hotel Notting Hill").
- Sister-hotel links in the nav (Chelsea House uses `http://`, and its certificate expired earlier) - check they still load.
