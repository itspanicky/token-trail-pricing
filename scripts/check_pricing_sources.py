#!/usr/bin/env python3

import hashlib
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


SOURCES = [
    "https://developers.openai.com/api/docs/models",
    "https://developers.openai.com/api/docs/models/gpt-5.6-sol",
    "https://platform.claude.com/docs/en/about-claude/pricing",
]


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ignored_depth = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "svg", "noscript"}:
            self.ignored_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "svg", "noscript"} and self.ignored_depth:
            self.ignored_depth -= 1

    def handle_data(self, data):
        if not self.ignored_depth:
            self.text.append(data)


def visible_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": "TokenTrailPricingMonitor/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        parser = VisibleTextParser()
        parser.feed(response.read().decode("utf-8", errors="replace"))
    return re.sub(r"\s+", " ", " ".join(parser.text)).strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_pricing_sources.py OUTPUT_PATH")

    result = {
        "sources": [
            {
                "url": url,
                "visibleTextSHA256": hashlib.sha256(visible_text(url).encode()).hexdigest(),
            }
            for url in SOURCES
        ]
    }
    Path(sys.argv[1]).write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
