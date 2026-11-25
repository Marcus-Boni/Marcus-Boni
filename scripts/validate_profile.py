"""Offline checks for the published profile. Python standard library only."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

from render_profile_header import (
    ASCII_SOURCE,
    OUTPUTS as HERO_OUTPUTS,
    build_svg as build_hero_svg,
)
from render_systems_blueprint import (
    OUTPUTS as BLUEPRINT_OUTPUTS,
    build_svg as build_blueprint_svg,
)

ROOT = Path(__file__).resolve().parents[1]
ALL_GENERATED = set(HERO_OUTPUTS.values()) | set(BLUEPRINT_OUTPUTS.values())
EXPECTED_SOURCES = {
    name for variant, name in HERO_OUTPUTS.items() if variant != (False, False)
} | {
    name for variant, name in BLUEPRINT_OUTPUTS.items() if variant != (False, False)
}
EXPECTED_IMGS = {
    HERO_OUTPUTS[(False, False)],
    BLUEPRINT_OUTPUTS[(False, False)],
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
        self.imgs: set[str] = set()
        self.images = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        assert tag not in {"script", "iframe", "style"}, f"Unsupported README tag: {tag}"
        for attribute in ("src", "href", "srcset"):
            value = attributes.get(attribute)
            if value:
                check_reference(value, self.document)
        if tag == "a" and attributes.get("href"):
            target = Path(urlsplit(attributes["href"]).path).name
            assert target not in ALL_GENERATED, "Keep direct asset links out of README anchors"
        if tag == "img":
            self.images += 1
            assert attributes.get("alt", "").strip(), "Image needs alternative text"
            src = attributes.get("src")
            if src:
                self.imgs.add(Path(urlsplit(src).path).name)
        if tag == "source":
            srcset = attributes.get("srcset")
            if srcset:
                self.sources.add(Path(srcset).name)


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
            assert parser.images == 2, f"Expected 2 figure images (hero + architecture), got {parser.images}"
            assert parser.imgs == EXPECTED_IMGS, f"Unexpected <img> fallbacks in {filename}: {parser.imgs}"
            assert parser.sources == EXPECTED_SOURCES, f"Unexpected <source> variants in {filename}: {parser.sources}"
            assert content.startswith("<picture>\n"), "Place the hero directly at the top"
            assert "https://marcusboni.com.br/blog" in content, f"Blog reference missing in {filename}"
            assert "contrib-heatmap.svg" not in content, "Do not duplicate native activity"
            assert "language-bar.svg" not in content, "Do not use language counts as expertise"
            approach_heading = "## Como construo" if filename.endswith("pt-BR.md") else "## How I build"
            assert content.index(approach_heading) > content.rindex("</details>"), "Keep the engineering approach visible"
            project_sets.append(set(re.findall(r"https://github.com/Marcus-Boni/[\w.-]+", content)))
    assert project_sets[0] == project_sets[1], "README languages must link the same projects"


def validate_common_svg_safety(asset: Path, actual: str, namespace: dict[str, str]) -> ET.Element:
    root = ET.fromstring(actual)
    assert root.get("role") == "img", f"Missing role=img in {asset.name}"
    for element in ("title", "desc"):
        node = root.find(f"svg:{element}", namespace)
        assert node is not None and node.text, f"Missing SVG {element}: {asset.name}"
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        assert tag not in {"script", "foreignObject", "image", "animate", "animateTransform"}, (
            f"Forbidden SVG tag <{tag}> in {asset.name}"
        )
        for name, value in node.attrib.items():
            local_name = name.rsplit("}", 1)[-1]
            assert not local_name.lower().startswith("on"), f"Event handlers are forbidden: {asset.name}"
            if local_name == "href":
                assert value.startswith("#"), f"SVG must not request external resources: {asset.name}"
    assert "@import" not in actual and "@font-face" not in actual, f"External CSS forbidden in {asset.name}"
    assert not re.search(r"url\(\s*['\"]?(?:https?:|//|data:)", actual), f"External url() forbidden in {asset.name}"
    style = root.findtext("svg:style", namespaces=namespace)
    assert style is not None, f"Missing <style> in {asset.name}"
    static_style, media_rule, motion_style = style.partition(
        "@media (prefers-reduced-motion: no-preference)"
    )
    assert media_rule, f"Missing prefers-reduced-motion media query in {asset.name}"
    assert "animation:" not in static_style, f"Animations must be gated by prefers-reduced-motion in {asset.name}"
    assert motion_style.strip(), f"Missing motion rules in {asset.name}"
    assert asset.stat().st_size < 75_000, f"Unexpectedly large SVG: {asset.name} ({asset.stat().st_size} bytes)"
    return root


def validate_assets() -> None:
    namespace = {"svg": "http://www.w3.org/2000/svg"}

    portrait = ROOT / "assets" / "chrome-portrait.png"
    with portrait.open("rb") as image:
        header = image.read(24)
    assert header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR", "Avatar must be a PNG"
    assert tuple(int.from_bytes(header[index : index + 4], "big") for index in (16, 20)) == (500, 500)
    assert portrait.stat().st_size < 1_000_000, "Avatar must fit GitHub's upload limit"

    expected_lines = [line.rstrip() for line in ASCII_SOURCE.read_text(encoding="ascii").splitlines()]
    for (mobile, light), filename in HERO_OUTPUTS.items():
        asset = ROOT / "assets" / filename
        actual = asset.read_text(encoding="utf-8")
        expected = build_hero_svg(mobile=mobile, light=light)
        assert actual == expected, f"Stale asset: {filename}; regenerate with scripts/render_profile_header.py"
        assert expected == build_hero_svg(mobile=mobile, light=light), "Hero generator must be deterministic"

        root = validate_common_svg_safety(asset, actual, namespace)
        style = root.findtext("svg:style", namespaces=namespace) or ""
        static_style, _, motion_style = style.partition("@media (prefers-reduced-motion: no-preference)")
        assert ".portrait-reflection,.portrait-glint,.scan-beam{display:none}" in static_style
        assert "@keyframes assemble" in motion_style and "@keyframes sweep" in motion_style
        assert "@keyframes raster-scan" in motion_style and "@keyframes cursor-blink" in motion_style
        assert root.find("svg:use[@href='#portrait-glyphs']", namespace) is not None

        portrait_lines = root.findall(".//svg:g[@id='portrait-glyphs']/svg:text", namespace)
        delays = [
            float(node.get("style", "").removeprefix("--row-delay:").removesuffix("s"))
            for node in portrait_lines
        ]
        assert delays == sorted(set(delays)), "Every portrait row must have a distinct delay in print order"
        assert len(portrait_lines) >= 30, "The ASCII portrait must keep enough detail"
        assert [line.text.rstrip() for line in portrait_lines if line.text] == expected_lines, (
            f"Portrait glyphs do not match the source grid: {filename}"
        )
        assert len({node.get("textLength") for node in portrait_lines}) == 1

    for (mobile, light), filename in BLUEPRINT_OUTPUTS.items():
        asset = ROOT / "assets" / filename
        actual = asset.read_text(encoding="utf-8")
        expected = build_blueprint_svg(mobile=mobile, light=light)
        assert actual == expected, f"Stale asset: {filename}; regenerate with scripts/render_systems_blueprint.py"
        assert expected == build_blueprint_svg(mobile=mobile, light=light), "Blueprint generator must be deterministic"

        root = validate_common_svg_safety(asset, actual, namespace)
        cards = root.findall(".//svg:g[@class]", namespace)
        layer_cards = [g for g in cards if "layer-card" in (g.get("class") or "")]
        assert len(layer_cards) == 4, f"Expected 4 architecture layer cards in {filename}, got {len(layer_cards)}"


def main() -> None:
    validate_documents()
    validate_assets()
    print(
        "PASS: local references, blog links, bilingual parity, 8 monochrome self-contained SVGs, and reproducible assets"
    )


if __name__ == "__main__":
    main()
