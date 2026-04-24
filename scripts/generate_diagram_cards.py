#!/usr/bin/env python3

from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "diagram_cards"
EX_FILE_GLOB = "hello_*/ex_file"

SECTION_RE = re.compile(r"^(\d+)\.\s+(.*)$")
PORT_RE = re.compile(r"\b(?:EXPOSE|PORT=)(\d+)\b")

LANGUAGE_NAMES = {
    "hello_rust": "Rust",
    "hello_go": "Go",
    "hello_python": "Python",
    "hello_javascript": "JavaScript",
    "hello_php": "PHP",
    "hello_csharp": "C#",
    "hello_java": "Java",
    "hello_dart": "Dart",
    "hello_bash": "Bash",
}

PROJECT_STYLES = {
    "hello_rust": ("#d97706", "#0f766e"),
    "hello_go": ("#0f766e", "#ea580c"),
    "hello_python": ("#15803d", "#ca8a04"),
    "hello_javascript": ("#ca8a04", "#dc2626"),
    "hello_php": ("#7c3aed", "#0891b2"),
    "hello_csharp": ("#16a34a", "#c2410c"),
    "hello_java": ("#dc2626", "#0f766e"),
    "hello_dart": ("#0284c7", "#16a34a"),
    "hello_bash": ("#65a30d", "#9333ea"),
}


def parse_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_title: str | None = None
    current_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        match = SECTION_RE.match(line)
        if match and not line.startswith(" "):
            if current_title is not None:
                sections[current_title] = trim_blank_lines(current_lines)
            current_title = match.group(2).strip()
            current_lines = []
            continue

        current_lines.append(line.rstrip())

    if current_title is not None:
        sections[current_title] = trim_blank_lines(current_lines)

    return sections


def trim_blank_lines(lines: list[str]) -> list[str]:
    trimmed = list(lines)
    while trimmed and not trimmed[0].strip():
        trimmed.pop(0)
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    return trimmed


def first_non_empty(lines: list[str], fallback: str = "") -> str:
    for line in lines:
        if line.strip():
            return line.strip()
    return fallback


def extract_port(sections: dict[str, list[str]]) -> str:
    for section_lines in sections.values():
        for line in section_lines:
            match = PORT_RE.search(line)
            if match:
                return match.group(1)
    return "n/a"


def wrap_preserving_indent(lines: list[str], max_chars: int) -> list[str]:
    wrapped_lines: list[str] = []
    for raw in lines:
        if not raw.strip():
            wrapped_lines.append("")
            continue

        indent_count = len(raw) - len(raw.lstrip(" "))
        indent = "  " * (indent_count // 4)
        text = raw.lstrip(" ")
        available = max(12, max_chars - len(indent))
        parts = textwrap.wrap(
            text,
            width=available,
            break_long_words=True,
            break_on_hyphens=False,
            replace_whitespace=False,
            drop_whitespace=False,
        )
        if not parts:
            parts = [""]
        wrapped_lines.extend(indent + part for part in parts)
    return wrapped_lines


def block_height(lines: list[str], width: int) -> int:
    wrapped = wrap_preserving_indent(lines, max_chars_for_width(width))
    return 56 + 24 + max(1, len(wrapped)) * 22 + 24


def max_chars_for_width(width: int) -> int:
    return max(18, (width - 48) // 8)


def svg_escape(text: str) -> str:
    return html.escape(text, quote=False)


def render_badge(x: int, y: int, label: str, fill: str) -> str:
    width = max(92, 22 + len(label) * 8)
    return "\n".join(
        [
            f'<rect x="{x}" y="{y}" width="{width}" height="30" rx="8" fill="{fill}" opacity="0.95" />',
            (
                f'<text x="{x + 14}" y="{y + 20}" font-family="Inter, Arial, sans-serif" '
                f'font-size="14" font-weight="700" fill="#f8fafc">{svg_escape(label)}</text>'
            ),
        ]
    )


def render_block(x: int, y: int, width: int, title: str, lines: list[str], accent: str) -> tuple[str, int]:
    wrapped = wrap_preserving_indent(lines, max_chars_for_width(width))
    height = 56 + 24 + max(1, len(wrapped)) * 22 + 24
    parts = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="8" fill="#1f2428" stroke="#3d464d" stroke-width="1.2" />',
        f'<rect x="{x}" y="{y}" width="{width}" height="56" rx="8" fill="{accent}" />',
        f'<rect x="{x}" y="{y + 48}" width="{width}" height="8" fill="{accent}" />',
        (
            f'<text x="{x + 20}" y="{y + 34}" font-family="Inter, Arial, sans-serif" '
            f'font-size="20" font-weight="800" fill="#f8fafc">{svg_escape(title)}</text>'
        ),
    ]

    line_y = y + 86
    for line in wrapped or [""]:
        parts.append(
            f'<text x="{x + 24}" y="{line_y}" font-family="Menlo, Consolas, monospace" '
            f'font-size="15" fill="#e5e7eb" xml:space="preserve">{svg_escape(line)}</text>'
        )
        line_y += 22

    return "\n".join(parts), height


def render_card(project_dir: Path) -> tuple[str, str]:
    ex_file_path = project_dir / "ex_file"
    sections = parse_sections(ex_file_path.read_text(encoding="utf-8").splitlines())
    project_name = project_dir.name
    language_name = LANGUAGE_NAMES.get(project_name, project_name)
    primary, secondary = PROJECT_STYLES.get(project_name, ("#0f766e", "#d97706"))
    port = extract_port(sections)

    command_line = first_non_empty(sections.get("Command", []), "docker build")
    context_lines = sections.get("Context", ["- no context listed"])
    real_world_lines = sections.get("Real World", ["No Real World section"])
    build_lines = sections.get("Build stage", ["No Build stage section"])
    runtime_lines = sections.get("Runtime stage", ["No Runtime stage section"])

    width = 1600
    margin = 48
    column_gap = 32
    column_width = (width - margin * 2 - column_gap) // 2
    top_y = 150

    left_blocks = [
        ("Real World", real_world_lines, primary),
        ("Command", [command_line], secondary),
        ("Context", context_lines, "#ca8a04"),
    ]
    right_blocks = [
        ("Build Stage", build_lines, "#16a34a"),
        ("Runtime Stage", runtime_lines, "#ea580c"),
    ]

    left_height = sum(block_height(lines, column_width) for _, lines, _ in left_blocks) + 24 * (len(left_blocks) - 1)
    right_height = sum(block_height(lines, column_width) for _, lines, _ in right_blocks) + 24 * (len(right_blocks) - 1)
    height = top_y + max(left_height, right_height) + 56

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#151819" />',
        f'<rect x="24" y="24" width="{width - 48}" height="{height - 48}" rx="8" fill="#181c1f" stroke="#333c42" stroke-width="1.5" />',
        f'<rect x="{margin}" y="44" width="{width - margin * 2}" height="2" fill="{primary}" opacity="0.9" />',
        (
            f'<text x="{margin}" y="82" font-family="Inter, Arial, sans-serif" '
            f'font-size="34" font-weight="900" fill="#f8fafc">{svg_escape(language_name)} Diagram Card</text>'
        ),
        (
            f'<text x="{margin}" y="116" font-family="Inter, Arial, sans-serif" '
            f'font-size="18" fill="#cbd5df">{svg_escape(project_name)}  |  generated from ex_file</text>'
        ),
        render_badge(margin + 860, 68, f"Port {port}", primary),
        render_badge(margin + 980, 68, "Docker Ready", secondary),
        render_badge(margin + 1140, 68, "SVG", "#374151"),
    ]

    current_y = top_y
    for title, lines, accent in left_blocks:
        block_svg, block_h = render_block(margin, current_y, column_width, title, lines, accent)
        parts.append(block_svg)
        current_y += block_h + 24

    current_y = top_y
    right_x = margin + column_width + column_gap
    for title, lines, accent in right_blocks:
        block_svg, block_h = render_block(right_x, current_y, column_width, title, lines, accent)
        parts.append(block_svg)
        current_y += block_h + 24

    parts.append("</svg>")
    return "\n".join(parts), language_name


def build_index(entries: list[tuple[str, str]]) -> str:
    cards = []
    for filename, label in entries:
        cards.append(
            f"""
            <a class="card" href="{filename}">
              <img src="{filename}" alt="{html.escape(label)} diagram card" />
              <span>{html.escape(label)}</span>
            </a>
            """.strip()
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Microservice Diagram Cards</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #151819;
      --panel: #1f2428;
      --border: #3d464d;
      --text: #f8fafc;
      --muted: #cbd5df;
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      padding: 32px;
      font-family: Inter, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 32px;
    }}
    p {{
      margin: 0 0 24px;
      color: var(--muted);
      font-size: 16px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
    }}
    .card {{
      display: block;
      padding: 14px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel);
      text-decoration: none;
      color: inherit;
    }}
    .card img {{
      width: 100%;
      height: auto;
      display: block;
      border-radius: 6px;
      border: 1px solid #2d353b;
      background: #101314;
    }}
    .card span {{
      display: block;
      margin-top: 12px;
      font-size: 15px;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <h1>Microservice Diagram Cards</h1>
  <p>SVG cards generated from each language project's ex_file.</p>
  <div class="grid">
    {"".join(cards)}
  </div>
</body>
</html>
"""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    entries: list[tuple[str, str]] = []

    for ex_file in sorted(ROOT.glob(EX_FILE_GLOB)):
        project_dir = ex_file.parent
        svg_text, label = render_card(project_dir)
        output_name = f"{project_dir.name}.svg"
        (OUTPUT_DIR / output_name).write_text(svg_text, encoding="utf-8")
        entries.append((output_name, label))

    index_html = build_index(entries)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")


if __name__ == "__main__":
    main()
