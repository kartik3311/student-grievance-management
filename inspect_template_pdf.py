from pypdf import PdfReader

p = r"C:\Users\KARTIKK\Desktop\Prateek_DE_CA2_144.pdf"
page = PdfReader(p).pages[0]
print("mediabox", page.mediabox)


def mul(m, n):
    return [
        m[0] * n[0] + m[1] * n[2],
        m[0] * n[1] + m[1] * n[3],
        m[2] * n[0] + m[3] * n[2],
        m[2] * n[1] + m[3] * n[3],
        m[4] * n[0] + m[5] * n[2] + n[4],
        m[4] * n[1] + m[5] * n[3] + n[5],
    ]


def visitor(text, cm, tm, font_dict, font_size):
    normalized = " ".join(text.split())
    if normalized and ("P r a t e e k" in normalized or "S h r i" in normalized or "Prateek" in normalized):
        actual = mul(tm, cm)
        print(repr(text))
        print("  tm", [round(v, 2) for v in tm], "cm", [round(v, 2) for v in cm])
        print("  actual", [round(v, 2) for v in actual], "size", round(font_size, 2))


page.extract_text(visitor_text=visitor)
