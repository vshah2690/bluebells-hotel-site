#!/usr/bin/env python3
"""SEO sanity check for the Hotel Bluebells static site (standard library only).

Checks every *.html page in the site root:
  lang set | exactly one canonical on the production domain | one <title> |
  one meta description | one <h1>, no skipped heading levels |
  every <img> has alt (and width/height, lazy/priority hints, file exists) |
  JSON-LD parses (FAQPage text matches the visible page text) |
  og/twitter tags present, og:url == canonical, og:image absolute + exists |
  no href="#" on buttons | internal links and #anchors resolve |
  every page is listed in sitemap.xml | robots.txt sane

Exit code 1 if anything FAILs.

href="#" booking buttons are PENDING items until the SiteMinder URL exists:
they are reported as warnings by default and become failures with --strict
(use --strict on launch day).

Usage:  python scripts/seo_check.py [--strict]
"""
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
PROD = "https://www.hotelbluebells.com/"
STRICT = "--strict" in sys.argv

fails, warns = [], []


def fail(page, msg):
    fails.append(f"{page}: {msg}")


def warn(page, msg):
    warns.append(f"{page}: {msg}")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.html_attrs = {}
        self.metas, self.links, self.imgs, self.anchors = [], [], [], []
        self.sources, self.ids = [], set()
        self.headings, self.titles, self.ldjson = [], [], []
        self._cur = None      # ("title"|"h1".."h6"|"ld"|"a", buffer/data)
        self.text = []        # visible text (no script/style)
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.html_attrs = a
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "img":
            self.imgs.append((line, a))
        elif tag == "source":
            self.sources.append((line, a))
        elif tag == "a":
            self.anchors.append((line, a, ""))
            self._cur = ("a", len(self.anchors) - 1)
        elif tag == "title":
            self._cur = ("title", [])
        elif re.fullmatch(r"h[1-6]", tag):
            self.headings.append((int(tag[1]), line, ""))
            self._cur = ("h", len(self.headings) - 1)
        elif tag == "script":
            self._skip += 1
            if a.get("type") == "application/ld+json":
                self._cur = ("ld", [], line)
        elif tag == "style":
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip = max(0, self._skip - 1)
            if self._cur and self._cur[0] == "ld":
                self.ldjson.append(("".join(self._cur[1]), self._cur[2]))
                self._cur = None
        elif tag == "title" and self._cur and self._cur[0] == "title":
            self.titles.append("".join(self._cur[1]))
            self._cur = None
        elif re.fullmatch(r"h[1-6]", tag) or tag == "a":
            self._cur = None

    def handle_data(self, data):
        if self._cur:
            k = self._cur[0]
            if k in ("title", "ld"):
                self._cur[1].append(data)
            elif k == "h":
                i = self._cur[1]
                lv, ln, t = self.headings[i]
                self.headings[i] = (lv, ln, t + data)
            elif k == "a":
                i = self._cur[1]
                ln, a, t = self.anchors[i]
                self.anchors[i] = (ln, a, t + data)
        if not self._skip:
            self.text.append(data)


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


def meta(p, key, val):
    return [m for m in p.metas if m.get(key) == val]


def local_file(ref):
    ref = unquote(ref.split("?")[0].split("#")[0])
    return ROOT / ref.lstrip("/")


def main():
    pages = sorted(ROOT.glob("*.html"), key=lambda x: (x.name != "index.html", x.name))
    parsed = {p.name: parse(p) for p in pages}
    rows = []
    staging = 0

    # sitemap
    sm_locs = set()
    sm_path = ROOT / "sitemap.xml"
    if not sm_path.exists():
        fail("sitemap.xml", "missing")
    else:
        try:
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            sm_locs = {e.text.strip() for e in ET.parse(sm_path).getroot().findall("s:url/s:loc", ns)}
        except ET.ParseError as e:
            fail("sitemap.xml", f"invalid XML: {e}")

    for name, p in parsed.items():
        raw = (ROOT / name).read_text(encoding="utf-8")
        expected = PROD if name == "index.html" else PROD + name

        # lang
        if not p.html_attrs.get("lang"):
            fail(name, "<html> has no lang")
        elif p.html_attrs["lang"] != "en-GB":
            warn(name, f"lang is {p.html_attrs['lang']!r}, expected 'en-GB'")

        # canonical
        canon = [l.get("href") for l in p.links if l.get("rel") == "canonical"]
        if len(canon) != 1:
            fail(name, f"{len(canon)} canonical tags (need exactly 1)")
        elif canon[0] != expected:
            fail(name, f"canonical is {canon[0]!r}, expected {expected!r}")

        # title / description
        if len(p.titles) != 1:
            fail(name, f"{len(p.titles)} <title> tags")
        title = norm(html.unescape(p.titles[0])) if p.titles else ""
        descs = meta(p, "name", "description")
        if len(descs) != 1:
            fail(name, f"{len(descs)} meta descriptions")
        desc = norm(descs[0].get("content", "")) if descs else ""
        if len(title) > 60:
            warn(name, f"title is {len(title)} chars (>60 may truncate)")
        if not 70 <= len(desc) <= 160:
            warn(name, f"meta description is {len(desc)} chars (aim for ~120-155)")
        rows.append((name, len(title), len(desc), title))

        # robots
        robots = [m.get("content", "") for m in meta(p, "name", "robots")]
        if not any("index, follow" in r for r in robots):
            fail(name, "production robots tag (index, follow, ...) missing")
        has_noindex = any("noindex" in r for r in robots)
        marked = "<!-- STAGING-NOINDEX-START -->" in raw and "<!-- STAGING-NOINDEX-END -->" in raw
        if has_noindex and not marked:
            fail(name, "noindex present but not wrapped in STAGING-NOINDEX markers (go-live.py cannot remove it)")
        staging += has_noindex

        # open graph / twitter
        for prop in ("og:type", "og:site_name", "og:locale", "og:title", "og:description", "og:url", "og:image"):
            if not meta(p, "property", prop):
                fail(name, f"missing {prop}")
        if not meta(p, "name", "twitter:card"):
            fail(name, "missing twitter:card")
        ogurl = meta(p, "property", "og:url")
        if ogurl and ogurl[0].get("content") != expected:
            fail(name, "og:url differs from canonical")
        ogimg = meta(p, "property", "og:image")
        if ogimg:
            u = ogimg[0].get("content", "")
            if not u.startswith(PROD):
                fail(name, f"og:image not on production domain: {u}")
            elif not local_file(u[len(PROD):]).is_file():
                fail(name, f"og:image file not found: {u}")
        ogd = meta(p, "property", "og:description")
        if ogd and descs and norm(ogd[0].get("content", "")) != desc:
            fail(name, "og:description differs from meta description")
        ogt = meta(p, "property", "og:title")
        if ogt and norm(html.unescape(ogt[0].get("content", ""))) != title:
            fail(name, "og:title differs from <title>")

        # headings
        levels = [h[0] for h in p.headings]
        if levels.count(1) != 1:
            fail(name, f"{levels.count(1)} <h1> tags (need exactly 1)")
        if levels and levels[0] != 1:
            fail(name, f"first heading is h{levels[0]}, expected h1")
        for (a, _, _), (b, ln, t) in zip(p.headings, p.headings[1:]):
            if b > a + 1:
                fail(name, f"heading skips h{a} -> h{b} at line {ln} ({norm(t)[:30]!r})")

        # images
        first_hero = True
        for ln, a in p.imgs:
            if "alt" not in a:
                fail(name, f"<img> without alt at line {ln}")
            src = a.get("src", "")
            if a.get("id") == "lightboxImg":
                continue  # filled in by the lightbox script
            if not src.startswith(("http://", "https://", "data:")) and not local_file(src).is_file():
                fail(name, f"image file missing: {src} (line {ln})")
            if not (a.get("width") and a.get("height")):
                fail(name, f"<img> without width/height at line {ln}: {src}")
            hero = "hero-media__el" in (a.get("class") or "")
            if hero and first_hero:
                first_hero = False
                if a.get("loading") == "lazy":
                    fail(name, "first hero image must not be lazy-loaded")
                if a.get("fetchpriority") != "high":
                    fail(name, "first hero image should have fetchpriority=high")
            elif not hero and a.get("loading") != "lazy":
                fail(name, f"below-the-fold image not lazy at line {ln}: {src}")
            if a.get("decoding") != "async":
                warn(name, f"<img> without decoding=async at line {ln}")
        for ln, a in p.sources:
            for cand in (a.get("srcset") or "").split(","):
                u = cand.strip().split(" ")[0]
                if u and not local_file(u).is_file():
                    fail(name, f"<source> file missing: {u} (line {ln})")

        # JSON-LD
        blocks = []
        for txt, ln in p.ldjson:
            try:
                blocks.append(json.loads(txt))
            except json.JSONDecodeError as e:
                fail(name, f"JSON-LD at line {ln} does not parse: {e}")
        types = []
        for b in blocks:
            t = b.get("@type")
            types.append(t)
            for bad in ("aggregateRating", "review"):
                if bad in b:
                    fail(name, f"JSON-LD contains {bad} (not wanted)")
            if t == "FAQPage":
                vis = norm(" ".join(p.text))
                for q in b.get("mainEntity", []):
                    for s in (q["name"], q["acceptedAnswer"]["text"]):
                        if norm(s) not in vis:
                            fail(name, f"FAQ schema text not found on page: {s[:50]!r}")
        if name in ("index.html", "contact.html") and "Hotel" not in types:
            fail(name, "missing Hotel JSON-LD")
        if name != "index.html" and "BreadcrumbList" not in types:
            fail(name, "missing BreadcrumbList JSON-LD")
        if name == "faq.html" and "FAQPage" not in types:
            fail(name, "missing FAQPage JSON-LD")
        if name.endswith(("-room.html", "-suite.html")) and "HotelRoom" not in types:
            fail(name, "missing HotelRoom JSON-LD")

        # links
        pending = []
        for ln, a, label in p.anchors:
            href = html.unescape(a.get("href") or "")
            cls = a.get("class") or ""
            if href == "#":
                what = norm(label) or a.get("aria-label", "?")
                pending.append((ln, what, "btn" in cls))
                continue
            if not href or re.match(r"(https?:|mailto:|tel:|javascript:)", href):
                if href.startswith("http://") and "hotelbluebells.com" in href:
                    fail(name, f"insecure own-domain link: {href}")
                continue
            u = urlparse(href)
            if href.startswith("#"):
                target, frag = name, href[1:]
            else:
                path = unquote(u.path)
                target = "index.html" if path in ("/", "") else path.lstrip("/")
                frag = u.fragment
            if not (ROOT / target).is_file():
                fail(name, f"broken internal link {href!r} at line {ln}")
                continue
            if frag:
                tp = parsed.get(target)
                if tp is not None and frag not in tp.ids:
                    fail(name, f"anchor #{frag} not found in {target} (link at line {ln})")

        if pending:
            btn = [x for x in pending if x[2]]
            other = [x for x in pending if not x[2]]
            for kind, items in (("booking button(s)", btn), ("other link(s)", other)):
                if items:
                    detail = ", ".join(f"L{ln} {w[:22]!r}" for ln, w, _ in items)
                    (fail if STRICT else warn)(name, f'PENDING {len(items)} href="#" {kind}: {detail}')

        # sitemap
        if sm_locs and expected not in sm_locs:
            fail(name, f"not listed in sitemap.xml ({expected})")

    expected_all = {PROD if n == "index.html" else PROD + n for n in parsed}
    for extra in sorted(sm_locs - expected_all):
        fail("sitemap.xml", f"lists a URL with no matching page: {extra}")

    # robots.txt
    rt = ROOT / "robots.txt"
    if not rt.exists():
        fail("robots.txt", "missing")
    else:
        t = rt.read_text(encoding="utf-8")
        if re.search(r"^\s*Disallow:\s*/\s*$", t, re.M):
            fail("robots.txt", "Disallow: / blocks the whole site")
        if f"Sitemap: {PROD}sitemap.xml" not in t:
            fail("robots.txt", "Sitemap line missing or wrong")

    # ---- report
    print(f"{'page':26} {'title':>5} {'desc':>5}  title text")
    for n, tl, dl, t in rows:
        print(f"{n:26} {tl:>5} {dl:>5}  {t}")
    print(f"\nStaging noindex present on {staging}/{len(parsed)} pages "
          f"({'expected until go-live' if staging else 'none - live mode'}).")
    if warns:
        print(f"\nWARNINGS ({len(warns)}):")
        for w in warns:
            print("  -", w)
    if fails:
        print(f"\nFAILED ({len(fails)}):")
        for f in fails:
            print("  x", f)
        sys.exit(1)
    print(f"\nOK: {len(parsed)} pages checked, 0 failures"
          + (f", {len(warns)} warnings" if warns else "") + ".")


if __name__ == "__main__":
    main()
