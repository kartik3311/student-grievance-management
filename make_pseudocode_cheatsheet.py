from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


SOURCE = Path(r"C:\Users\KARTIKK\Desktop\CS401L_Unit_Wise_Pseudocode_Questions&Solutions.pdf")
OUTPUT = Path(r"C:\Users\KARTIKK\Desktop\CS401L_Pseudocode_A4_Cheat_Sheet.pdf")


def clean_text(value: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2190": "<-",
        "\u2026": "...",
        "\ufb01": "fi",
        "\ufb02": "fl",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")


def extract_blocks() -> list[tuple[str, list[str]]]:
    reader = PdfReader(str(SOURCE))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    text = clean_text(text)

    section_pattern = re.compile(r"^\s*(\d+\.\d+\.\s+.+?)\s*$", re.MULTILINE)
    sections = list(section_pattern.finditer(text))
    blocks: list[tuple[str, list[str]]] = []

    for index, match in enumerate(sections):
        title = match.group(1).strip()
        start = match.end()
        end = sections[index + 1].start() if index + 1 < len(sections) else len(text)
        chunk = text[start:end]
        pseudo_match = re.search(
            r"(?ims)^\s*Pseudocode\s*\n(.*?)(?=^\s*Complexity\s*:)",
            chunk,
        )
        if not pseudo_match:
            continue
        code = pseudo_match.group(1)
        code = re.sub(r"(?m)^P a g e\s+\|\s+\d+\s*$", "", code)
        code = re.sub(r"(?m)^CS401L - Unit Wise Pseudocode Solutions\s*$", "", code)
        lines = [line.rstrip() for line in code.splitlines()]

        compact: list[str] = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            compact.append(line)
        blocks.append((title, compact))

    return blocks


def wrap_code_line(line: str, font_name: str, font_size: float, max_width: float) -> list[str]:
    if not line:
        return [""]
    indent = len(line) - len(line.lstrip(" "))
    continuation = " " * min(indent + 4, 14)
    words = line.split(" ")
    pieces: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if stringWidth(trial, font_name, font_size) <= max_width:
            current = trial
            continue
        if current:
            pieces.append(current)
            current = continuation + word
        else:
            pieces.append(word)
            current = ""
    if current:
        pieces.append(current)
    return pieces


def draw_cheatsheet(blocks: list[tuple[str, list[str]]]) -> None:
    page_width, page_height = landscape(A4)
    margin_x = 18
    margin_top = 22
    margin_bottom = 18
    gutter = 10
    columns = 3
    col_width = (page_width - 2 * margin_x - gutter * (columns - 1)) / columns

    c = canvas.Canvas(str(OUTPUT), pagesize=landscape(A4))
    title_font = "Helvetica-Bold"
    code_font = "Courier"
    heading_size = 7.4
    code_size = 6.15
    line_height = 7.05
    title_gap = 1.8
    block_gap = 3.5
    usable_bottom = margin_bottom

    page_no = 1
    col = 0
    y = page_height - margin_top

    def start_page() -> None:
        c.setFont("Helvetica-Bold", 8)
        c.drawString(margin_x, page_height - 12, "CS401L Pseudocode Cheat Sheet")
        c.setFont("Helvetica", 7)
        c.drawRightString(page_width - margin_x, page_height - 12, f"A4 landscape - page {page_no}")
        c.setLineWidth(0.25)
        c.line(margin_x, page_height - 16, page_width - margin_x, page_height - 16)

    def next_column_or_page() -> None:
        nonlocal col, y, page_no
        col += 1
        if col >= columns:
            c.showPage()
            page_no += 1
            col = 0
            start_page()
        y = page_height - margin_top

    start_page()

    for title, raw_lines in blocks:
        wrapped_lines: list[str] = []
        for raw in raw_lines:
            wrapped_lines.extend(wrap_code_line(raw, code_font, code_size, col_width))

        title_height = heading_size + title_gap
        code_height = len(wrapped_lines) * line_height
        total_height = title_height + code_height + block_gap

        if y - total_height < usable_bottom and y < page_height - margin_top:
            next_column_or_page()

        x = margin_x + col * (col_width + gutter)
        c.setFont(title_font, heading_size)
        c.drawString(x, y, title)
        y -= heading_size + title_gap

        c.setFont(code_font, code_size)
        for line in wrapped_lines:
            if y - line_height < usable_bottom:
                next_column_or_page()
                x = margin_x + col * (col_width + gutter)
                c.setFont(title_font, heading_size)
                c.drawString(x, y, f"{title} (cont.)")
                y -= heading_size + title_gap
                c.setFont(code_font, code_size)
            c.drawString(x, y, line)
            y -= line_height
        y -= block_gap

    c.save()


if __name__ == "__main__":
    items = extract_blocks()
    if len(items) != 28:
        raise SystemExit(f"Expected 28 pseudocode blocks, found {len(items)}")
    draw_cheatsheet(items)
    print(OUTPUT)
