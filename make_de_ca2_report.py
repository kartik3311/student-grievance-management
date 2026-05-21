from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\KARTIKK\Desktop\Cracks")
INPUT_CSV = Path(r"C:\Users\KARTIKK\Desktop\New folder\BigMart Sales.csv")
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_PDF = OUTPUT_DIR / "DE_CA2_completed.pdf"


NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#0E7C7B")
GOLD = colors.HexColor("#F2A541")
RED = colors.HexColor("#C44536")
GREEN = colors.HexColor("#3A7D44")
LIGHT = colors.HexColor("#F4F7FA")
GRID = colors.HexColor("#D9E2EC")
TEXT = colors.HexColor("#202833")
MUTED = colors.HexColor("#5C6B7A")


def fmt_money(value):
    return f"{value:,.0f}"


def shorten(text, max_width, font="Helvetica", size=7):
    if stringWidth(str(text), font, size) <= max_width:
        return str(text)
    out = str(text)
    while out and stringWidth(out + "...", font, size) > max_width:
        out = out[:-1]
    return out + "..."


class DashboardFlowable(Flowable):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.width = 7.2 * inch
        self.height = 5.8 * inch

    def wrap(self, avail_width, avail_height):
        self.width = min(avail_width, 7.2 * inch)
        return self.width, self.height

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height

        c.setFillColor(colors.white)
        c.roundRect(0, 0, w, h, 8, stroke=0, fill=1)
        c.setStrokeColor(GRID)
        c.roundRect(0, 0, w, h, 8, stroke=1, fill=0)

        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(18, h - 26, "Dashboard Snapshot - BigMart Sales CSV")

        # Filter chips
        chips = ["Region: All", "Category: All", "Year: All"]
        x = 18
        for chip in chips:
            chip_w = stringWidth(chip, "Helvetica", 8) + 18
            c.setFillColor(LIGHT)
            c.setStrokeColor(GRID)
            c.roundRect(x, h - 50, chip_w, 18, 5, stroke=1, fill=1)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 8)
            c.drawString(x + 8, h - 43, chip)
            x += chip_w + 8

        left_w = (w - 54) * 0.62
        right_w = w - 54 - left_w
        top_y = h - 76
        self._panel(c, 18, top_y - 190, left_w, 190, "MRP Trend by Outlet Establishment Year")
        self._line_chart(
            c,
            36,
            top_y - 170,
            left_w - 36,
            132,
            list(self.data["year_sum"].index),
            list(self.data["year_sum"].values),
            TEAL,
        )

        self._panel(c, 36 + left_w, top_y - 190, right_w, 190, "MRP by Region")
        self._bar_chart(
            c,
            54 + left_w,
            top_y - 166,
            right_w - 36,
            118,
            list(self.data["region_sum"].index),
            list(self.data["region_sum"].values),
            [TEAL, GOLD, GREEN],
            vertical=True,
        )

        self._panel(c, 18, 24, w - 36, 190, "Average MRP by Category")
        self._hbar_chart(
            c,
            36,
            49,
            w - 72,
            138,
            list(self.data["category_mean"].index),
            list(self.data["category_mean"].values),
        )

    def _panel(self, c, x, y, w, h, title):
        c.setFillColor(colors.HexColor("#FBFCFE"))
        c.setStrokeColor(GRID)
        c.roundRect(x, y, w, h, 6, stroke=1, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 10, y + h - 18, title)

    def _line_chart(self, c, x, y, w, h, labels, values, color):
        min_v, max_v = min(values), max(values)
        span = max_v - min_v or 1
        left, bottom = x + 24, y + 22
        chart_w, chart_h = w - 42, h - 42
        c.setStrokeColor(GRID)
        c.setLineWidth(0.5)
        for i in range(4):
            yy = bottom + chart_h * i / 3
            c.line(left, yy, left + chart_w, yy)
        pts = []
        for i, val in enumerate(values):
            xx = left + chart_w * i / (len(values) - 1)
            yy = bottom + ((val - min_v) / span) * chart_h
            pts.append((xx, yy))
        c.setStrokeColor(color)
        c.setLineWidth(2)
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1])
        c.setFillColor(color)
        for xx, yy in pts:
            c.circle(xx, yy, 2.4, stroke=0, fill=1)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.8)
        for i, lab in enumerate(labels):
            xx = left + chart_w * i / (len(labels) - 1)
            c.drawCentredString(xx, bottom - 12, str(lab))
        c.drawRightString(left - 4, bottom + chart_h - 3, fmt_money(max_v))
        c.drawRightString(left - 4, bottom - 1, fmt_money(min_v))

    def _bar_chart(self, c, x, y, w, h, labels, values, palette, vertical=True):
        max_v = max(values) or 1
        left, bottom = x + 18, y + 18
        chart_w, chart_h = w - 28, h - 36
        bar_w = chart_w / len(values) * 0.55
        gap = chart_w / len(values)
        c.setStrokeColor(GRID)
        c.setLineWidth(0.5)
        c.line(left, bottom, left + chart_w, bottom)
        for i, (lab, val) in enumerate(zip(labels, values)):
            bh = chart_h * val / max_v
            bx = left + gap * i + (gap - bar_w) / 2
            c.setFillColor(palette[i % len(palette)])
            c.roundRect(bx, bottom, bar_w, bh, 2, stroke=0, fill=1)
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 7)
            c.drawCentredString(bx + bar_w / 2, bottom - 12, str(lab))
            c.drawCentredString(bx + bar_w / 2, bottom + bh + 5, fmt_money(val))

    def _hbar_chart(self, c, x, y, w, h, labels, values):
        max_v = max(values) or 1
        rows = len(values)
        row_h = h / rows
        label_w = 108
        bar_w = w - label_w - 42
        for i, (lab, val) in enumerate(zip(labels, values)):
            yy = y + h - (i + 1) * row_h + 3
            fill = TEAL if i >= rows - 4 else GOLD if i <= 3 else colors.HexColor("#8AA7B8")
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 6.8)
            c.drawRightString(x + label_w - 6, yy + 3, shorten(lab, label_w - 8))
            c.setFillColor(colors.HexColor("#E8EEF3"))
            c.roundRect(x + label_w, yy, bar_w, 7, 2, stroke=0, fill=1)
            c.setFillColor(fill)
            c.roundRect(x + label_w, yy, bar_w * val / max_v, 7, 2, stroke=0, fill=1)
            c.setFillColor(TEXT)
            c.setFont("Helvetica", 6.8)
            c.drawString(x + label_w + bar_w + 5, yy + 1, f"{val:.1f}")


def build_data():
    df = pd.read_csv(INPUT_CSV)
    year_sum = df.groupby("Outlet_Establishment_Year")["Item_MRP"].sum().sort_index()
    region_sum = df.groupby("Outlet_Location_Type")["Item_MRP"].sum().sort_index()
    category_mean = df.groupby("Item_Type")["Item_MRP"].mean().sort_values()
    category_sum = df.groupby("Item_Type")["Item_MRP"].sum().sort_values()
    return {
        "df": df,
        "year_sum": year_sum,
        "region_sum": region_sum,
        "category_mean": category_mean,
        "category_sum": category_sum,
        "region_mean": df.groupby("Outlet_Location_Type")["Item_MRP"].mean().sort_values(),
        "outlet_mean": df.groupby("Outlet_Type")["Item_MRP"].mean().sort_values(),
    }


def make_styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "TitleCenter",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=29,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceAfter=10,
        )
    )
    base.add(
        ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            textColor=MUTED,
            spaceAfter=24,
        )
    )
    base.add(
        ParagraphStyle(
            "H1x",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "H2x",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=TEAL,
            spaceBefore=8,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "Bodyx",
            parent=base["BodyText"],
            fontSize=9.8,
            leading=14,
            textColor=TEXT,
            spaceAfter=7,
            alignment=TA_LEFT,
        )
    )
    base.add(
        ParagraphStyle(
            "Notex",
            parent=base["BodyText"],
            fontSize=8.8,
            leading=12.5,
            textColor=colors.HexColor("#405261"),
            backColor=colors.HexColor("#EEF5F8"),
            borderColor=colors.HexColor("#BBD5DE"),
            borderWidth=0.6,
            borderPadding=7,
            spaceAfter=10,
        )
    )
    return base


def make_table(rows, widths):
    table = Table(rows, colWidths=widths, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.4),
                ("LEADING", (0, 0), (-1, -1), 10.5),
                ("TEXTCOLOR", (0, 1), (-1, -1), TEXT),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
                ("GRID", (0, 0), (-1, -1), 0.35, GRID),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.42 * inch, "DE CA-2 completed report")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    data = build_data()
    df = data["df"]
    styles = make_styles()

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        rightMargin=0.62 * inch,
        leftMargin=0.62 * inch,
        topMargin=0.62 * inch,
        bottomMargin=0.62 * inch,
        title="DE CA-2 Completed Report",
        author="Codex",
    )

    story = []
    story.append(Spacer(1, 0.25 * inch))
    story.append(Paragraph("DE CA-2", styles["TitleCenter"]))
    story.append(
        Paragraph(
            "Completed answers and dashboard-backed analysis using the provided BigMart Sales.csv",
            styles["Subtitle"],
        )
    )

    story.append(
        Paragraph(
            "<b>Data note:</b> The supplied CSV has 5,681 rows and 11 fields, but it does not include actual "
            "Sales, Profit, transaction Date/Month, or a named Region column. Therefore, the dashboard below uses "
            "available substitutes: <b>Item_MRP</b> as the value measure, <b>Item_Type</b> as category, "
            "<b>Outlet_Location_Type</b> as region, and <b>Outlet_Establishment_Year</b> as the time field. "
            "True monthly sales trend, seasonality, and profit/loss conclusions require those missing fields.",
            styles["Notex"],
        )
    )

    key_rows = [
        ["Metric", "Value"],
        ["Rows in dataset", f"{len(df):,}"],
        ["Value measure used", "Item_MRP"],
        ["Highest average MRP category", f"{data['category_mean'].idxmax()} ({data['category_mean'].max():.2f})"],
        ["Lowest average MRP category", f"{data['category_mean'].idxmin()} ({data['category_mean'].min():.2f})"],
        ["Highest total MRP location tier", f"{data['region_sum'].idxmax()} ({fmt_money(data['region_sum'].max())})"],
        ["Lowest average MRP location tier", f"{data['region_mean'].idxmin()} ({data['region_mean'].min():.2f})"],
    ]
    story.append(make_table(key_rows, [2.35 * inch, 4.05 * inch]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Part A: Dashboard", styles["H1x"]))
    story.append(DashboardFlowable(data))
    story.append(PageBreak())

    story.append(Paragraph("Part A: Answers", styles["H1x"]))
    qa = [
        (
            "Q1. Identify Trend",
            "Using the available time field, Outlet_Establishment_Year, the value measure fluctuates rather than "
            "showing a steady increase or decrease. Total Item_MRP is highest for outlets established in 1985, "
            "drops in some later establishment years, and rises again around 2007. The average MRP by year is also "
            "fairly stable, mostly between about 138 and 143, so the visual does not show a strong upward sales trend.",
        ),
        (
            "Q2. Identify Seasonality",
            "Monthly seasonality cannot be reliably identified from the supplied BigMart CSV because there is no "
            "transaction date, month, or monthly sales column. A correct seasonality conclusion would need monthly "
            "sales values over multiple years. With only outlet establishment year, there is no evidence for "
            "consistent high or low months.",
        ),
        (
            "Q3. Business Insight",
            "Actual profit and loss cannot be calculated because the CSV does not contain Profit, Cost, Quantity, "
            "or Sales fields. Using average Item_MRP only as a weak proxy, Baking Goods has the lowest average MRP "
            f"({data['category_mean'].min():.2f}), while Tier 2 has the slightly lowest average MRP by location "
            f"({data['region_mean'].min():.2f}). Recommendation: collect actual sales and profit/margin data, then "
            "review pricing, promotions, and assortment for lower-performing categories before calling any segment loss-making.",
        ),
    ]
    for q, answer in qa:
        story.append(KeepTogether([Paragraph(q, styles["H2x"]), Paragraph(answer, styles["Bodyx"])]))

    story.append(Spacer(1, 0.12 * inch))
    cat_rows = [["Category", "Average MRP", "Total MRP", "Rows"]]
    cat_summary = (
        df.groupby("Item_Type")["Item_MRP"]
        .agg(["mean", "sum", "count"])
        .sort_values("mean")
        .reset_index()
    )
    for _, row in cat_summary.head(6).iterrows():
        cat_rows.append([row["Item_Type"], f"{row['mean']:.2f}", fmt_money(row["sum"]), f"{int(row['count']):,}"])
    story.append(Paragraph("Lowest average MRP categories", styles["H2x"]))
    story.append(make_table(cat_rows, [2.3 * inch, 1.25 * inch, 1.3 * inch, 0.8 * inch]))
    story.append(PageBreak())

    story.append(Paragraph("Part B: Time-Series Forecasting", styles["H1x"]))
    part_b = [
        (
            "Q4. Why is stationarity important before applying ARIMA?",
            "Stationarity is important because ARIMA works best when the statistical properties of the series, "
            "such as mean, variance, and autocorrelation, remain stable over time. If the data has trend or "
            "seasonality, the model may learn misleading relationships and produce unreliable forecasts. "
            "Differencing is commonly used to make a non-stationary series more stationary before fitting ARIMA.",
        ),
        (
            "Q5. Difference between ARIMA and SARIMA",
            "ARIMA models non-seasonal time-series behavior using autoregressive, differencing, and moving average "
            "terms: ARIMA(p, d, q). SARIMA extends ARIMA by adding seasonal terms: SARIMA(p, d, q)(P, D, Q, s). "
            "SARIMA is preferred when the series has a repeating seasonal cycle, such as weekly demand patterns, "
            "monthly yearly cycles, or annual holiday peaks.",
        ),
        (
            "Q6. Case study: E-commerce sales forecasting",
            "SARIMA should be chosen for this scenario. The sales series has an increasing trend and a repeating "
            "seasonal pattern where sales rise sharply every November and December, then fall after December and "
            "repeat the same way each year. ARIMA can handle trend after differencing, but it does not explicitly "
            "model the repeating yearly seasonal effect. SARIMA is better because it includes both non-seasonal "
            "and seasonal components. The 'S' in SARIMA stands for Seasonal; for monthly sales data, the seasonal "
            "period would typically be 12 months.",
        ),
    ]
    for q, answer in part_b:
        story.append(KeepTogether([Paragraph(q, styles["H2x"]), Paragraph(answer, styles["Bodyx"])]))

    story.append(Spacer(1, 0.15 * inch))
    model_rows = [
        ["Scenario feature", "Model implication"],
        ["Steady increasing trend", "Use differencing to stabilize the series."],
        ["Repeating November-December spike", "Use seasonal terms with period 12."],
        ["Need 6-month forecast", "Fit SARIMA and forecast the next six monthly points."],
        ["Inventory planning", "Use forecasts plus safety stock before the festive months."],
    ]
    story.append(make_table(model_rows, [2.4 * inch, 3.95 * inch]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return OUTPUT_PDF


if __name__ == "__main__":
    print(build_pdf())
