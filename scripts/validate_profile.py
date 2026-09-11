"""Offline checks for the published profile. Python standard library only."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from render_profile_header import build_svg

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = {
    "profile-header.svg": (False, False),
    "profile-header-light.svg": (False, True),
    "profile-header-mobile.svg": (True, False),
    "profile-header-mobile-light.svg": (True, True),
}


def check_reference(reference: str, document: Path) -> None:
    target = urlsplit(reference)
    if target.scheme or target.netloc or not target.path:
        return
    path = (document.parent / unquote(target.path)).resolve()
    assert path.is_relative_to(ROOT), f"Reference escapes repository: {reference}"
    assert path.is_file(), f"Missing local reference in {document.name}: {reference}"


class ProfileHTML(HTMLParser):
    def __init__(self, document: Path) -> None:
        super().__init__()
        self.document = document
        self.sources: set[str] = set()
        self.images = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        assert tag not in {"script", "iframe", "style"}, f"Unsupported README tag: {tag}"
        for attribute in ("src", "href", "srcset"):
            value = attributes.get(attribute)
            if value:
                check_reference(value, self.document)
        if tag == "img":
            self.images += 1
            assert attributes.get("alt", "").strip(), "Image needs alternative text"
        if tag == "source":
            self.sources.add(Path(attributes["srcset"]).name)


def validate_documents() -> None:
    project_sets = []
    for filename in ("README.md", "README.pt-BR.md", "PROFILE.md", "DESIGN.md"):
        document = ROOT / filename
        content = document.read_text(encoding="utf-8-sig")
        for reference in re.findall(r"\]\(([^\s)]+)\)", content):
            check_reference(reference, document)
        if filename.startswith("README"):
            parser = ProfileHTML(document)
            parser.feed(content)
            assert parser.images == 1, "Keep one header image and native text for the body"
            assert len(parser.sources) == 3, "Expected mobile and light header sources"
            assert "contrib-heatmap.svg" not in content, "Do not duplicate native activity"
            assert "language-bar.svg" not in content, "Do not use language counts as expertise"
            project_sets.append(set(re.findall(r"https://github.com/Marcus-Boni/[\w.-]+", content)))
    assert project_sets[0] == project_sets[1], "README languages must link the same projects"


def validate_assets() -> None:
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    for filename, (mobile, light) in VARIANTS.items():
        asset = ROOT / "assets" / filename
        actual = asset.read_text(encoding="utf-8")
        expected = build_svg(mobile=mobile, light=light)
        assert actual == expected, f"Stale asset: {filename}; regenerate the headers"
        assert expected == build_svg(mobile=mobile, light=light), "Generator must be deterministic"
        root = ET.fromstring(actual)
        assert root.get("role") == "img"
        for element in ("title", "desc"):
            node = root.find(f"svg:{element}", namespace)
            assert node is not None and node.text, f"Missing SVG {element}: {filename}"
        for node in root.iter():
            tag = node.tag.rsplit("}", 1)[-1]
            assert tag not in {"script", "foreignObject", "image", "animate", "animateTransform"}
            for name, value in node.attrib.items():
                local_name = name.rsplit("}", 1)[-1]
                assert not local_name.lower().startswith("on"), "Event handlers are forbidden"
                if local_name == "href":
                    assert value.startswith("#"), "SVG must not request external resources"
        assert "@import" not in actual and "@font-face" not in actual
        assert not re.search(r"url\(\s*['\"]?(?:https?:|//|data:)", actual)
        assert asset.stat().st_size < 75_000, f"Unexpectedly large header: {filename}"


def main() -> None:
    validate_documents()
    validate_assets()
    print("PASS: local references, bilingual project parity, accessible self-contained SVGs, and reproducible assets")


if __name__ == "__main__":
    main()
