"""Assemble editable HTML fragments into one offline-readable portfolio page."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
from collections import Counter
import argparse
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUTPUT = ROOT / "dist" / "index.html"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}

def read_fragment(relative):
    path = (CONTENT / relative).resolve()
    if CONTENT.resolve() not in path.parents or not path.is_file():
        raise ValueError("Invalid content file: " + relative)
    return path.read_text(encoding="utf-8-sig").strip()

def body_length(card):
    body = card.split('class="detail-content"', 1)[-1]
    return len(re.sub(r"\s+", "", unescape(re.sub(r"<[^>]+>", "", body))))

def collection_html(name, settings):
    cards = [read_fragment(path) for path in settings["items"]]
    if settings.get("sort") == "body-length-desc":
        cards.sort(key=body_length, reverse=True)
    elif settings.get("sort", "manual") != "manual":
        raise ValueError("Unknown collection sort: " + name)
    if name == "professional":
        cards = [re.sub(r"PRODUCTION EXPERIENCE / \d+",
                        "PRODUCTION EXPERIENCE / %02d" % (i + 1), card, count=1)
                 for i, card in enumerate(cards)]
    return read_fragment(settings["header"]) + "\n" + "\n".join(cards) + "\n</div>\n</section>"

class ValidatePage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = []
        self.anchors = []
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for key in ("src", "href", "data-full-image"):
            value = attrs.get(key, "")
            if not value:
                continue
            if key == "href" and value.startswith("#"):
                if len(value) > 1:
                    self.anchors.append(value[1:])
            elif not urlsplit(value).scheme and not value.startswith("//"):
                self.assets.append(value.split("#")[0].split("?")[0])
        if attrs.get("srcset"):
            self.assets.extend(item.strip().split()[0]
                               for item in attrs["srcset"].split(",") if item.strip())

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            raise ValueError("Unbalanced HTML near </%s>: %s" % (tag, self.stack[-5:]))
        self.stack.pop()

    def finish(self):
        if self.stack:
            raise ValueError("Unclosed elements: " + repr(self.stack))
        duplicates = [key for key, count in Counter(self.ids).items() if count > 1]
        if duplicates:
            raise ValueError("Duplicate IDs: " + repr(duplicates))
        missing_anchors = set(self.anchors) - set(self.ids)
        if missing_anchors:
            raise ValueError("Missing anchors: " + repr(missing_anchors))
        missing_assets = []
        for relative in self.assets:
            if not relative or urlsplit(relative).scheme or relative.startswith("//"):
                continue
            path = (OUTPUT.parent / relative).resolve()
            if OUTPUT.parent.resolve() not in path.parents or not path.is_file():
                missing_assets.append(relative)
        if missing_assets:
            raise ValueError("Missing local assets: " + repr(sorted(set(missing_assets))))

def render():
    config = json.loads(read_fragment("site.json"))
    pieces = []
    for name in config["layout"]:
        if name in config["sections"]:
            pieces.append(read_fragment(config["sections"][name]))
        elif name in config["collections"]:
            pieces.append(collection_html(name, config["collections"][name]))
        else:
            raise ValueError("Unknown layout entry: " + name)
    shell = read_fragment("page.html")
    marker = "<!-- PORTFOLIO_CONTENT -->"
    if shell.count(marker) != 1:
        raise ValueError("Expected exactly one page content marker")
    result = shell.replace(marker, "\n".join(pieces)) + "\n"
    validator = ValidatePage()
    validator.feed(result)
    validator.finish()
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="Validate fragments and verify dist/index.html without writing files")
    args = parser.parse_args()
    result = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8-sig") != result:
            raise SystemExit("dist/index.html is stale. Run: python build.py")
        print("PASS: fragments, HTML structure, IDs, local assets, and generated page are current.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(result, encoding="utf-8")
        print("Built dist/index.html. No PDF files generated.")

if __name__ == "__main__":
    main()

