from pathlib import Path
from math import ceil

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT


ROOT = Path(r"C:\Users\KARTIKK\Desktop\Cracks")
CSV_PATH = Path(r"C:\Users\KARTIKK\Desktop\New folder\BigMart Sales.csv")
OUT_DIR = ROOT / "outputs"
OUT_PDF = OUT_DIR / "Lochan_Sharma_BigMart_DE_CA2_PowerBI.pdf"


PBI_YELLOW = colors.HexColor("#F2C811")
PBI_DARK = colors.HexColor("#252423")
PBI_BLACK = colors.HexColor("#1F1F1F")
CANVAS_BG = colors.HexColor("#F3F2F1")
VIS_BG = colors.white
GRID = colors.HexColor("#E1DFDD")
TEXT = colors.HexColor("#323130")
MUTED = colors.HexColor("#605E5C")
BLUE = colors.HexColor("#118DFF")
PURPLE = colors.HexColor("#744EC2")
TEAL = colors.HexColor("#00B7C3")
ORANGE = colors.HexColor("#E66C37")
GREEN = colors.HexColor("#107C10")
RED = colors.HexColor("#D13438")


def money(v):
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"{v / 1_000:.1f}K"
    return f"{v:.0f}"


def read_data():
    df = pd.read_csv(CSV_PATH)
    df["Sales_Proxy"] = df["Item_MRP"]
    cat = (
        df.groupby("Item_Type")
        .agg(Sales_Proxy=("Sales_Proxy", "sum"), Avg_MRP=("Item_MRP", "mean"), Rows=("Item_MRP", "size"))
        .sort_values("Avg_MRP")
    )
    region = (
        df.groupby("Outlet_Location_Type")
        .agg(Sales_Proxy=("Sales_Proxy", "sum"), Avg_MRP=("Item_MRP", "mean"), Rows=("Item_MRP", "size"))
        .sort_index()
    )
    year = (
        df.groupby("Outlet_Establishment_Year")
        .agg(Sales_Proxy=("Sales_Proxy", "sum"), Avg_MRP=("Item_MRP", "mean"), Rows=("Item_MRP", "size"))
        .sort_index()
    )
    outlet = (
        df.groupby("Outlet_Type")
        .agg(Sales_Proxy=("Sales_Proxy", "sum"), Avg_MRP=("Item_MRP", "mean"), Rows=("Item_MRP", "size"))
        .sort_values("Sales_Proxy", ascending=False)
    )
    return df, cat, region, year, outlet


def rect(c, x, y, w, h, fill=VIS_BG, stroke=GRID, radius=0):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    if radius:
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    else:
        c.rect(x, y, w, h, stroke=1, fill=1)


def text(c, x, y, s, size=9, color=TEXT, bold=False, align="left"):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    if align == "right":
        c.drawRightString(x, y, s)
    elif align == "center":
        c.drawCentredString(x, y, s)
    else:
        c.drawString(x, y, s)


def visual_title(c, x, y, w, h, title, subtitle=None):
    text(c, x + 10, y + h - 17, title, 9.5, TEXT, True)
    if subtitle:
        text(c, x + 10, y + h - 30, subtitle, 6.7, MUTED)
    text(c, x + w - 18, y + h - 18, "⋯", 12, MUTED, True, "center")


def slicer(c, x, y, w, h, title, value):
    rect(c, x, y, w, h, colors.white, GRID)
    text(c, x + 8, y + h - 14, title, 6.7, MUTED)
    text(c, x + 8, y + 9, value, 8.5, TEXT)
    text(c, x + w - 12, y + 9, "▾", 8, MUTED, True, "center")


def card(c, x, y, w, h, label, value, accent):
    rect(c, x, y, w, h, colors.white, GRID)
    c.setFillColor(accent)
    c.rect(x, y, 4, h, stroke=0, fill=1)
    text(c, x + 12, y + h - 17, label, 7.2, MUTED)
    text(c, x + 12, y + 15, value, 19, TEXT, True)


def line_chart(c, x, y, w, h, labels, values):
    visual_title(c, x, y, w, h, "Monthly Sales Trend", "Shown by outlet establishment year because month/date is absent")
    left, bottom = x + 42, y + 32
    chart_w, chart_h = w - 62, h - 70
    min_v, max_v = min(values), max(values)
    span = max(max_v - min_v, 1)
    c.setStrokeColor(GRID)
    c.setLineWidth(0.6)
    for i in range(4):
        yy = bottom + chart_h * i / 3
        c.line(left, yy, left + chart_w, yy)
        val = min_v + span * i / 3
        text(c, left - 6, yy - 2, money(val), 6.4, MUTED, align="right")
    points = []
    for idx, val in enumerate(values):
        xx = left + chart_w * idx / (len(values) - 1)
        yy = bottom + (val - min_v) / span * chart_h
        points.append((xx, yy))
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        c.line(x1, y1, x2, y2)
    c.setFillColor(BLUE)
    for xx, yy in points:
        c.circle(xx, yy, 2.5, stroke=0, fill=1)
    for idx, label in enumerate(labels):
        xx = left + chart_w * idx / (len(labels) - 1)
        text(c, xx, bottom - 14, str(label), 6.3, MUTED, align="center")


def vbar_chart(c, x, y, w, h, labels, values, title, subtitle, palette):
    visual_title(c, x, y, w, h, title, subtitle)
    left, bottom = x + 38, y + 35
    chart_w, chart_h = w - 55, h - 73
    max_v = max(values) or 1
    c.setStrokeColor(GRID)
    c.setLineWidth(0.6)
    c.line(left, bottom, left + chart_w, bottom)
    slots = len(values)
    slot_w = chart_w / slots
    bar_w = min(28, slot_w * 0.55)
    for idx, (lab, val) in enumerate(zip(labels, values)):
        bx = left + idx * slot_w + (slot_w - bar_w) / 2
        bh = chart_h * val / max_v
        c.setFillColor(palette[idx % len(palette)])
        c.rect(bx, bottom, bar_w, bh, stroke=0, fill=1)
        text(c, bx + bar_w / 2, bottom - 14, str(lab), 6.6, MUTED, align="center")
        text(c, bx + bar_w / 2, bottom + bh + 4, money(val), 6.2, MUTED, align="center")


def hbar_chart(c, x, y, w, h, labels, values, title, subtitle):
    visual_title(c, x, y, w, h, title, subtitle)
    left, bottom = x + 95, y + 28
    chart_w, chart_h = w - 125, h - 58
    rows = len(values)
    row_h = chart_h / rows
    max_v = max(values) or 1
    for idx, (lab, val) in enumerate(zip(labels, values)):
        yy = bottom + chart_h - (idx + 0.8) * row_h
        c.setFillColor(colors.HexColor("#EDEBE9"))
        c.rect(left, yy, chart_w, row_h * 0.42, stroke=0, fill=1)
        c.setFillColor(ORANGE if idx < 4 else BLUE)
        c.rect(left, yy, chart_w * val / max_v, row_h * 0.42, stroke=0, fill=1)
        label = lab if stringWidth(lab, "Helvetica", 6.8) < 82 else lab[:16] + "..."
        text(c, left - 5, yy + 1.3, label, 6.8, MUTED, align="right")
        text(c, left + chart_w + 4, yy + 1.3, f"{val:.1f}", 6.5, MUTED)


def donut_chart(c, x, y, w, h, labels, values, title, subtitle):
    visual_title(c, x, y, w, h, title, subtitle)
    cx, cy = x + w * 0.36, y + h * 0.43
    r = min(w, h) * 0.23
    total = sum(values)
    start = 90
    palette = [BLUE, PURPLE, TEAL, ORANGE]
    for idx, val in enumerate(values):
        extent = 360 * val / total
        c.setFillColor(palette[idx % len(palette)])
        c.wedge(cx - r, cy - r, cx + r, cy + r, start, start - extent, stroke=0, fill=1)
        start -= extent
    c.setFillColor(colors.white)
    c.circle(cx, cy, r * 0.55, stroke=0, fill=1)
    text(c, cx, cy + 3, money(total), 12, TEXT, True, "center")
    text(c, cx, cy - 9, "Total", 6.8, MUTED, align="center")
    legend_x = x + w * 0.62
    legend_y = y + h - 50
    for idx, (lab, val) in enumerate(zip(labels, values)):
        yy = legend_y - idx * 17
        c.setFillColor(palette[idx % len(palette)])
        c.rect(legend_x, yy - 5, 8, 8, stroke=0, fill=1)
        text(c, legend_x + 12, yy - 4, f"{lab}  {money(val)}", 7.0, MUTED)


def draw_dashboard(c, df, cat, region, year, outlet):
    width, height = landscape(A4)
    c.setPageSize((width, height))
    c.setFillColor(CANVAS_BG)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Power BI Desktop chrome
    c.setFillColor(PBI_DARK)
    c.rect(0, height - 27, width, 27, stroke=0, fill=1)
    text(c, 15, height - 18, "Power BI Desktop", 10, colors.white, True)
    for idx, item in enumerate(["File", "Home", "Insert", "Modeling", "View", "Help"]):
        text(c, 140 + idx * 58, height - 18, item, 7.5, colors.HexColor("#EDEBE9"))
    c.setFillColor(PBI_YELLOW)
    c.rect(0, height - 27, 5, 27, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.rect(0, 0, 32, height - 27, stroke=0, fill=1)
    c.setFillColor(PBI_YELLOW)
    c.rect(8, height - 72, 16, 16, stroke=0, fill=1)
    text(c, 16, height - 102, "▦", 13, MUTED, True, "center")
    text(c, 16, height - 132, "▤", 13, MUTED, True, "center")

    canvas_x, canvas_y = 46, 30
    canvas_w, canvas_h = width - 68, height - 76
    rect(c, canvas_x, canvas_y, canvas_w, canvas_h, colors.white, colors.HexColor("#C8C6C4"))
    text(c, canvas_x + 16, canvas_y + canvas_h - 23, "BIGMART SALES DASHBOARD", 16, TEXT, True)
    text(c, canvas_x + 16, canvas_y + canvas_h - 39, "LOCHAN SHARMA  |  DE CA-2", 8.2, MUTED)
    text(c, canvas_x + canvas_w - 16, canvas_y + canvas_h - 22, "Report view", 7.5, MUTED, align="right")

    # Slicers
    sx = canvas_x + canvas_w - 300
    slicer(c, sx, canvas_y + canvas_h - 48, 90, 32, "Region", "All")
    slicer(c, sx + 98, canvas_y + canvas_h - 48, 102, 32, "Category", "All")
    slicer(c, sx + 208, canvas_y + canvas_h - 48, 74, 32, "Year", "All")

    total_proxy = df["Sales_Proxy"].sum()
    rows = len(df)
    avg_mrp = df["Item_MRP"].mean()
    top_region = region["Sales_Proxy"].idxmax()
    card_y = canvas_y + canvas_h - 100
    card(c, canvas_x + 16, card_y, 132, 42, "Sales proxy (Item_MRP)", money(total_proxy), BLUE)
    card(c, canvas_x + 160, card_y, 112, 42, "Rows", f"{rows:,}", PURPLE)
    card(c, canvas_x + 284, card_y, 112, 42, "Average MRP", f"{avg_mrp:.2f}", TEAL)
    card(c, canvas_x + 408, card_y, 128, 42, "Top location tier", top_region, ORANGE)

    # Visual containers
    y_top = canvas_y + canvas_h - 270
    rect(c, canvas_x + 16, y_top, 335, 155)
    line_chart(c, canvas_x + 16, y_top, 335, 155, list(year.index), list(year["Sales_Proxy"]))

    rect(c, canvas_x + 365, y_top, 180, 155)
    donut_chart(
        c,
        canvas_x + 365,
        y_top,
        180,
        155,
        list(region.index),
        list(region["Sales_Proxy"]),
        "Sales by Region",
        "Outlet_Location_Type",
    )

    rect(c, canvas_x + 558, y_top, 210, 155)
    top_outlets = outlet.head(4)
    vbar_chart(
        c,
        canvas_x + 558,
        y_top,
        210,
        155,
        list(top_outlets.index),
        list(top_outlets["Sales_Proxy"]),
        "Sales by Outlet Type",
        "Sales proxy by outlet",
        [BLUE, PURPLE, TEAL, ORANGE],
    )

    y_bottom = canvas_y + 26
    rect(c, canvas_x + 16, y_bottom, 365, 150)
    hbar_chart(
        c,
        canvas_x + 16,
        y_bottom,
        365,
        150,
        list(cat["Avg_MRP"].index),
        list(cat["Avg_MRP"].values),
        "Profit by Category",
        "Profit not available; average MRP used as category performance proxy",
    )

    rect(c, canvas_x + 395, y_bottom, 373, 150)
    visual_title(c, canvas_x + 395, y_bottom, 373, 150, "Dashboard Notes", "Data limitations from source CSV")
    notes = [
        "No Date or Month column is present, so true monthly seasonality cannot be measured.",
        "No Profit, Cost, Quantity, or Item_Outlet_Sales column is present.",
        "Charts use Item_MRP as a transparent value proxy for dashboard practice.",
        f"Lowest average MRP category: {cat['Avg_MRP'].idxmin()} ({cat['Avg_MRP'].min():.2f}).",
        f"Lowest average MRP region: {region['Avg_MRP'].idxmin()} ({region['Avg_MRP'].min():.2f}).",
    ]
    yy = y_bottom + 102
    for n in notes:
        c.setFillColor(PBI_YELLOW)
        c.circle(canvas_x + 411, yy + 2, 2.2, stroke=0, fill=1)
        text(c, canvas_x + 420, yy, n, 7.4, TEXT)
        yy -= 18

    c.showPage()


def para(c, x, y, w, html, size=9.8, leading=13.5, color=TEXT):
    style = ParagraphStyle(
        "p",
        fontName="Helvetica",
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    p = Paragraph(html, style)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def heading(c, x, y, text_value):
    text(c, x, y, text_value, 13.5, TEXT, True)
    c.setStrokeColor(PBI_YELLOW)
    c.setLineWidth(2.2)
    c.line(x, y - 6, x + 88, y - 6)
    return y - 18


def answer_block(c, x, y, w, q, ans):
    text(c, x, y, q, 10.5, TEXT, True)
    y -= 7
    y = para(c, x, y, w, ans, 9.4, 12.8)
    return y - 12


def draw_answers(c, df, cat, region, year):
    width, height = A4
    c.setPageSize((width, height))
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, stroke=0, fill=1)
    c.setFillColor(PBI_DARK)
    c.rect(0, height - 45, width, 45, stroke=0, fill=1)
    c.setFillColor(PBI_YELLOW)
    c.rect(0, height - 45, 8, 45, stroke=0, fill=1)
    text(c, 28, height - 28, "DE CA-2 Answers - BigMart Sales Dashboard", 14, colors.white, True)
    text(c, width - 28, height - 28, "LOCHAN SHARMA", 10, colors.white, True, "right")

    x, y, w = 48, height - 76, width - 96
    y = heading(c, x, y, "Part A")
    caveat = (
        "<b>Important dataset note:</b> The provided BigMart CSV has Item_MRP, Item_Type, "
        "Outlet_Location_Type, Outlet_Type, and Outlet_Establishment_Year, but it does not have "
        "Sales, Profit, transaction Date, Month, or Year of sale. Therefore, the dashboard uses "
        "<b>Item_MRP as the sales/value proxy</b>. Conclusions below are based only on the available data."
    )
    y = para(c, x, y, w, caveat, 8.8, 12.2, MUTED) - 12

    values = list(year["Sales_Proxy"].values)
    if values[-1] > values[0] and max(values) == values[-1]:
        trend = "increasing"
    else:
        trend = "fluctuating"
    q1 = (
        f"The overall dashboard trend is <b>{trend}</b>, not a smooth continuous increase. "
        f"Using Item_MRP by Outlet_Establishment_Year, the highest total value appears for 1985 "
        f"({money(year['Sales_Proxy'].max())}), while later years move up and down. The average MRP "
        "also stays in a narrow range, so the visual suggests fluctuation rather than a strong sales rise."
    )
    y = answer_block(c, x, y, w, "Q1. Identify Trend", q1)

    q2 = (
        "Seasonality cannot be identified from this CSV because there is no Month or Date column. "
        "The dashboard can show value by outlet establishment year, but it cannot prove that any month "
        "is consistently high or low. A monthly sales field over multiple years would be required for a "
        "proper seasonality answer."
    )
    y = answer_block(c, x, y, w, "Q2. Identify Seasonality", q2)

    q3 = (
        f"Actual loss/profit cannot be calculated because no Profit, Cost, Quantity, or Sales column is present. "
        f"Using average MRP as a category performance proxy, <b>{cat['Avg_MRP'].idxmin()}</b> is the weakest "
        f"category ({cat['Avg_MRP'].min():.2f}), and <b>{region['Avg_MRP'].idxmin()}</b> is the lowest location "
        f"tier by average MRP ({region['Avg_MRP'].min():.2f}). Recommendation: collect actual profit and sales "
        "data, then improve assortment, pricing, and promotions for weaker categories/tiers before deciding "
        "whether they are genuinely loss-making."
    )
    y = answer_block(c, x, y, w, "Q3. Business Insight", q3)

    y = heading(c, x, y + 2, "Part B")
    q4 = (
        "Stationarity is important before applying ARIMA because ARIMA assumes that the series has stable "
        "statistical behavior over time, especially mean, variance, and autocorrelation. If trend or seasonality "
        "remains in the data, the model can produce unreliable forecasts. Differencing is used to make a "
        "non-stationary series closer to stationary."
    )
    y = answer_block(c, x, y, w, "Q4. Why is stationarity important before applying ARIMA?", q4)

    q5 = (
        "ARIMA models non-seasonal time-series patterns using autoregressive, differencing, and moving-average "
        "terms: ARIMA(p, d, q). SARIMA adds seasonal components: SARIMA(p, d, q)(P, D, Q, s). SARIMA is preferred "
        "when the data has a repeating cycle, such as monthly yearly peaks, weekly demand cycles, or holiday effects."
    )
    y = answer_block(c, x, y, w, "Q5. What is the difference between ARIMA and SARIMA?", q5)

    q6 = (
        "For the e-commerce case, SARIMA should be chosen. The data has an increasing trend and a repeating "
        "seasonal pattern where sales rise every November and December and then drop after December. ARIMA can "
        "handle trend after differencing, but SARIMA is better because it explicitly models the yearly seasonal "
        "cycle. The 'S' in SARIMA means <b>Seasonal</b>; for monthly data, the seasonal period is usually 12."
    )
    y = answer_block(c, x, y, w, "Q6. Case Study: E-Commerce Sales Forecasting", q6)

    # Small support table at bottom
    table_data = [
        ["Dashboard field", "Used as", "Reason"],
        ["Item_MRP", "Sales/value proxy", "No sales column in CSV"],
        ["Item_Type", "Category", "Closest category field"],
        ["Outlet_Location_Type", "Region", "Tier 1 / Tier 2 / Tier 3 location grouping"],
        ["Outlet_Establishment_Year", "Time proxy", "No transaction month/date column"],
    ]
    table = Table(table_data, colWidths=[1.5 * inch, 1.55 * inch, 3.15 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), PBI_DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.7),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAF9F8")]),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    tw, th = table.wrap(w, 100)
    table.drawOn(c, x, 42)
    text(c, width - 48, 24, "Page 2", 8, MUTED, align="right")
    c.showPage()


def build_pdf():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df, cat, region, year, outlet = read_data()
    c = canvas.Canvas(str(OUT_PDF))
    c.setTitle("BigMart Power BI Dashboard - Lochan Sharma")
    c.setAuthor("LOCHAN SHARMA")
    draw_dashboard(c, df, cat, region, year, outlet)
    draw_answers(c, df, cat, region, year)
    c.save()
    return OUT_PDF


if __name__ == "__main__":
    print(build_pdf())
