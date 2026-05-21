import re
from pypdf import PdfReader

p = r"C:\Users\KARTIKK\Desktop\Prateek_DE_CA2_144.pdf"
reader = PdfReader(p)
page = reader.pages[0]


def parse_tounicode(stream):
    if not stream:
        return {}
    data = stream.get_data().decode("latin1", errors="ignore")
    cmap = {}
    for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", data):
        try:
            cmap[int(src, 16)] = bytes.fromhex(dst).decode("utf-16-be")
        except Exception:
            pass
    return cmap


def maps_from_resources(resources):
    maps = {}
    if resources and "/Font" in resources:
        for name, font_ref in resources["/Font"].items():
            font = font_ref.get_object()
            tu = font.get("/ToUnicode")
            maps[str(name)] = parse_tounicode(tu.get_object() if tu else None)
    return maps


font_maps = maps_from_resources(page["/Resources"])
for name, m in font_maps.items():
    print(name, "map", len(m))


def decode_hex(hexs, cmap):
    b = bytes.fromhex(hexs)
    out = []
    for i in range(0, len(b), 2):
        code = int.from_bytes(b[i : i + 2], "big")
        out.append(cmap.get(code, f"?{code:04X}"))
    return "".join(out)


for name, obj in page["/Resources"]["/XObject"].items():
    x = obj.get_object()
    if not hasattr(x, "get_data"):
        continue
    data = x.get_data().decode("latin1", errors="ignore")
    if " Tj" not in data:
        continue
    local_maps = {**font_maps, **maps_from_resources(x.get("/Resources"))}
    fonts = re.findall(r"/(F\d+)\s+[\d.]+\s+Tf", data)
    font = "/" + fonts[-1] if fonts else None
    cmap = local_maps.get(font, {})
    text = ""
    for hx in re.findall(r"<([0-9A-Fa-f]+)>\s*Tj", data):
        text += decode_hex(hx, cmap)
    if "Prateek" in text or "P r a" in text or "Shriv" in text:
        print("MATCH", name, "font", font, repr(text))
        print(data)
    elif text.strip():
        print(name, "font", font, repr(text[:80]))
