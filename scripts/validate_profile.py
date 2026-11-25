"""Offline checks for the published profile. Python standard library only."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from render_profile_header import ASCII_SOURCE, OUTPUTS, build_svg

ROOT = Path(__file__).resolve().parents[1]



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
            assert parser.sources == {name for variant, name in OUTPUTS.items() if variant != (False, False)}
            assert f'./assets/{OUTPUTS[False, False]}?raw=true' in content, "Provide a replay link"
            assert "contrib-heatmap.svg" not in content, "Do not duplicate native activity"
            assert "language-bar.svg" not in content, "Do not use language counts as expertise"
            approach_heading = "## Como construo" if filename.endswith("pt-BR.md") else "## How I build"
            assert content.index(approach_heading) > content.index("</details>"), "Keep the engineering approach visible"
            project_sets.append(set(re.findall(r"https://github.com/Marcus-Boni/[\w.-]+", content)))
    assert project_sets[0] == project_sets[1], "README languages must link the same projects"


def validate_assets() -> None:
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    portrait = ROOT / "assets" / "chrome-portrait.png"
    with portrait.open("rb") as image:
        header = image.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR", "Avatar must be a PNG"
    assert tuple(int.from_bytes(header[index:index + 4], "big") for index in (16, 20)) == (500, 500)
    assert portrait.stat().st_size < 1_000_000, "Avatar must fit GitHub's upload limit"
    for (mobile, light), filename in OUTPUTS.items():
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
        style = root.findtext("svg:style", namespaces=namespace)
        static_style, media_rule, motion_style = style.partition(
            "@media (prefers-reduced-motion: no-preference)"
        )
        assert media_rule and "animation:" not in static_style
        assert ".portrait-reflection{display:none}" in static_style
        assert "@keyframes assemble" in motion_style and "@keyframes sweep" in motion_style
        assert "infinite" not in motion_style
        assert root.find("svg:use[@href='#portrait-glyphs']", namespace) is not None
        portrait_lines = root.findall(".//svg:g[@id='portrait-glyphs']/svg:text", namespace)
        delays = [float(node.get("style").removeprefix("--row-delay:").removesuffix("s")) for node in portrait_lines]
        assert delays == sorted(set(delays)), "Every portrait row must have a distinct delay in print order"
        assert len(portrait_lines) >= 30, "The ASCII portrait must keep enough detail"
        assert [line.text.rstrip() for line in portrait_lines] == [
            line.rstrip() for line in ASCII_SOURCE.read_text(encoding="ascii").splitlines()
        ], f"Portrait glyphs do not match the source grid: {filename}"
        assert len({node.get("textLength") for node in portrait_lines}) == 1
        assert asset.stat().st_size < 75_000, f"Unexpectedly large header: {filename}"


def main() -> None:
    validate_documents()
    validate_assets()
    print("PASS: local references, bilingual project parity, accessible self-contained SVGs, and reproducible assets")


if __name__ == "__main__":
    main()
