"""Check generated pages for missing assets, links and heading anchors."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "_site"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.headings = 0
        self.errors = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f'Duplicate id: {attrs["id"]}')
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("Image missing alt text")
        for attribute in ("href", "src"):
            if attrs.get(attribute):
                self.links.append(attrs[attribute])


def check():
    pages = {p.resolve(): Page(p) for p in ROOT.glob("*.html")}
    if not pages:
        raise SystemExit("No pages found. Run scripts/build_site.py first.")
    errors = []
    for path, page in pages.items():
        errors.extend(f"{path.name}: {error}" for error in page.errors)
        if page.headings != 1:
            errors.append(f"{path.name}: expected one h1, got {page.headings}")
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                errors.append(f"{path.name}: missing or outside-site link {link}")
                continue
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.name}: missing anchor {link}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} pages: headings, local links, anchors and image alt text OK.")


if __name__ == "__main__":
    check()
