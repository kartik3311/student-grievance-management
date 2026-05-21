from pypdf import PdfReader

p = r"C:\Users\KARTIKK\Desktop\Prateek_DE_CA2_144.pdf"
reader = PdfReader(p)
page = reader.pages[0]
data = page.get_contents().get_data()
for pat in [b"177.84", b"796.8", b"12 Tf", b"Tj", b"TJ", b"/F"]:
    print(pat, data.find(pat))
for start in range(0, len(data), 3000):
    chunk = data[start : start + 3000]
    if b"Tj" in chunk or b"TJ" in chunk or b"Tf" in chunk:
        print("\n---", start, "---")
        print(chunk[:3000])

print("resources", page["/Resources"].keys())
if "/XObject" in page["/Resources"]:
    for name, obj in page["/Resources"]["/XObject"].items():
        x = obj.get_object()
        print("xobject", name, x.get("/Subtype"), x.get("/Width"), x.get("/Height"))
        if hasattr(x, "get_data"):
            xd = x.get_data()
            print("  len", len(xd), "has Tj", b"Tj" in xd, "has TJ", b"TJ" in xd, "has Tf", b"Tf" in xd)
            for pat in [b"177.84", b"796.8", b"Tj", b"TJ", b"Tf"]:
                print(" ", pat, xd.find(pat))
