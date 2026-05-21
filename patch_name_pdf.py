from pathlib import Path
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


INPUT = Path(r"C:\Users\KARTIKK\Desktop\Prateek_DE_CA2_144.pdf")
OUTPUT = Path(r"C:\Users\KARTIKK\Desktop\Cracks\outputs\Lochan_Sharma_DE_CA2.pdf")


def make_overlay(page_width, page_height):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # The source PDF is an A4 Canva export. The original name is positioned
    # near the top-left of page 1 at this coordinate; cover only that text run.
    c.setFillColor(colors.white)
    c.rect(172, 785, 190, 24, stroke=0, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11.5)
    c.drawString(177.8, 794.8, "LOCHAN SHARMA")

    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(INPUT))
    writer = PdfWriter()

    for idx, page in enumerate(reader.pages):
        if idx == 0:
            # The old name is drawn inside form XObject /X57. Blank it so the
            # template no longer contains the previous name as hidden text.
            xobjects = page["/Resources"].get("/XObject", {})
            if "/X57" in xobjects:
                xobjects["/X57"].get_object().set_data(b"")
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            overlay = make_overlay(width, height)
            page.merge_page(overlay)
        writer.add_page(page)

    writer.add_metadata(
        {
            "/Title": "DE CA-2 - Lochan Sharma",
            "/Author": "LOCHAN SHARMA",
            "/Creator": "Codex",
            "/Producer": "pypdf + reportlab",
        }
    )
    with OUTPUT.open("wb") as f:
        writer.write(f)
    print(OUTPUT)


if __name__ == "__main__":
    main()
