"""MOCKUP PDF: Displacement Snapshot layout preview - illustrative data only.

Adapted from the approved climate-profile-generator layout (Corporate Navy,
UN blue masthead). All figures are placeholders for layout review only.
"""
import io
from datetime import datetime

import pymupdf
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as canvas_module
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, Image,
                                KeepTogether, NextPageTemplate, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

FONT_DIR = "../fonts/"
pdfmetrics.registerFont(TTFont("Roboto Condensed", FONT_DIR + "RobotoCondensed-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Roboto Condensed Bold", FONT_DIR + "RobotoCondensed-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Roboto Condensed Italic", FONT_DIR + "RobotoCondensed-Italic.ttf"))
registerFontFamily("Roboto Condensed", normal="Roboto Condensed",
                   bold="Roboto Condensed Bold", italic="Roboto Condensed Italic",
                   boldItalic="Roboto Condensed Bold")

# ━━ Palette: approved UN blue family (as climate-profile-generator) ━━
UN_BLUE = colors.HexColor("#24356B")
UN_DARK = colors.HexColor("#1F3A7A")
TABLE_STRIPE = colors.HexColor("#EEF1F8")
BORDER = colors.HexColor("#C5CEDF")
TEXT_PRIMARY = colors.HexColor("#20201d")
TEXT_MUTED = colors.HexColor("#8b8982")
M, P = TEXT_MUTED, TEXT_PRIMARY
PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm
CONTENT_W = PAGE_W - 2 * MARGIN
BAND_H = 4.4 * cm
TOP_BAND_LATER = 0.9 * cm
BOTTOM = 1.8 * cm
GENERATED = datetime.now().strftime("%d %b %Y, %H:%M")
CREDIT = "Built by Omar Farooq  |  github.com/ahaomar/displacement-snapshot-generator"
TOTAL_PAGES = [1]

h2 = ParagraphStyle("h2", fontName="Roboto Condensed Bold", fontSize=13, leading=17,
                    textColor=UN_DARK, spaceBefore=14, spaceAfter=6)
body = ParagraphStyle("body", fontName="Roboto Condensed", fontSize=11, leading=16.5,
                      textColor=P, alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle("bullet", fontName="Roboto Condensed", fontSize=11, leading=16.5,
                        textColor=P, leftIndent=14, spaceAfter=3)
foot = ParagraphStyle("foot", fontName="Roboto Condensed", fontSize=8.5, leading=12,
                      textColor=M, leftIndent=24, firstLineIndent=-24, spaceAfter=2)
caption = ParagraphStyle("caption", fontName="Roboto Condensed", fontSize=8.5, leading=11,
                         textColor=M, alignment=TA_CENTER, spaceBefore=4, spaceAfter=4)
banner_txt = ParagraphStyle("banner", fontName="Roboto Condensed Bold", fontSize=8, leading=10,
                            textColor=colors.white, alignment=TA_CENTER)
stat_style = ParagraphStyle("stat", fontName="Roboto Condensed Bold", fontSize=17, leading=20,
                            textColor=UN_DARK, alignment=TA_CENTER)
label_style = ParagraphStyle("statlabel", fontName="Roboto Condensed", fontSize=8.5,
                             leading=11, textColor=M, alignment=TA_CENTER)


def draw_footer(cv, page_num):
    cv.saveState()
    cv.setStrokeColor(BORDER)
    cv.setLineWidth(0.6)
    cv.line(MARGIN, 1.45 * cm, PAGE_W - MARGIN, 1.45 * cm)
    cv.setFont("Roboto Condensed", 7.5)
    cv.setFillColor(M)
    cv.drawString(MARGIN, 1.05 * cm, CREDIT)
    right = "Generated %s   |   Page %s of %s" % (GENERATED, page_num, TOTAL_PAGES[0])
    cv.drawRightString(PAGE_W - MARGIN, 1.05 * cm, right)
    cv.restoreState()


def on_first(cv, doc):
    cv.saveState()
    cv.setFillColor(UN_BLUE)
    cv.rect(0, PAGE_H - BAND_H, PAGE_W, BAND_H, stroke=0, fill=1)
    cv.setFillColor(colors.HexColor("#1B2852"))
    cv.rect(0, PAGE_H - BAND_H, PAGE_W, 0.18 * cm, stroke=0, fill=1)
    cv.setFont("Roboto Condensed Bold", 8.5)
    cv.setFillColor(colors.Color(1, 1, 1, alpha=0.75))
    cv.drawString(MARGIN, PAGE_H - 1.15 * cm, "C O U N T R Y   B R I E F")
    cv.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.15 * cm, "MOCKUP PREVIEW")
    cv.setFillColor(colors.white)
    cv.setFont("Roboto Condensed Bold", 21)
    cv.drawString(MARGIN, PAGE_H - 2.25 * cm, "Displacement Snapshot")
    cv.setFont("Roboto Condensed", 13)
    cv.setFillColor(colors.Color(1, 1, 1, alpha=0.92))
    cv.drawString(MARGIN, PAGE_H - 3.05 * cm,
                  "Sudan  |  Cross-border movement into Chad")
    cv.setFont("Roboto Condensed", 9)
    cv.setFillColor(colors.Color(1, 1, 1, alpha=0.8))
    cv.drawString(MARGIN, PAGE_H - 3.75 * cm,
                  "5-year trend  |  October 2026  |  Displacement Snapshot Generator")
    cv.restoreState()
    draw_footer(cv, 1)


def on_later(cv, doc):
    cv.saveState()
    cv.setFillColor(UN_BLUE)
    cv.rect(0, PAGE_H - TOP_BAND_LATER, PAGE_W, TOP_BAND_LATER, stroke=0, fill=1)
    cv.setFont("Roboto Condensed Bold", 8.5)
    cv.setFillColor(colors.white)
    cv.drawString(MARGIN, PAGE_H - 0.62 * cm,
                  "Displacement Snapshot  |  Sudan  (MOCKUP)")
    cv.restoreState()
    draw_footer(cv, doc.page)


def stat(v, l):
    t = Table([[Paragraph("<b>%s</b>" % v, stat_style)], [Paragraph(l, label_style)]],
              colWidths=[(CONTENT_W - 24) / 3.0])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TABLE_STRIPE),
        ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
        ("LINEABOVE", (0, 0), (-1, 0), 2, UN_BLUE),
        ("TOPPADDING", (0, 0), (-1, 0), 8), ("BOTTOMPADDING", (-1, -1), (-1, -1), 8),
        ("TOPPADDING", (0, -1), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
    ]))
    return t


def embed(path, max_w=CONTENT_W * 0.86):
    w, h = PILImage.open(path).size
    r = min(max_w / w, 1.0)
    return Image(path, width=w * r, height=h * r)


def make_story():
    story = [NextPageTemplate('Later')]
    banner = Table([[Paragraph("MOCKUP  -  LAYOUT PREVIEW  -  ALL DATA ILLUSTRATIVE",
                               banner_txt)]], colWidths=[CONTENT_W])
    banner.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), UN_DARK),
                                ("TOPPADDING", (0, 0), (-1, -1), 4),
                                ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story.append(banner)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Key Figures</b>", h2))
    row = Table([[stat("4.7M", "people displaced within Sudan"),
                  stat("1.9M", "refugees & returnees crossing borders"),
                  stat("+154%", "IDP growth since 2019")]],
                colWidths=[CONTENT_W / 3.0] * 3, hAlign="CENTER")
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                             ("LEFTPADDING", (0, 0), (-1, -1), 4),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    story.append(row)
    story.append(Spacer(1, 6))
    story.append(Paragraph("Every figure in this brief is footnoted with its source, URL and "
                           "retrieval date. In a real run all numbers are fetched live from "
                           "the cited open databases; anything unavailable is flagged, never "
                           "estimated.", body))

    story.append(Paragraph("<b>1. Displacement overview</b>", h2))
    story.append(Paragraph(
        "Sudan remains one of the world's largest displacement crises. Internal displacement "
        "has grown sharply over the five-year observation window, with the steepest increase "
        "from 2023 onwards (Figure 1). Cross-border movement into neighbouring countries - "
        "principally Chad, South Sudan and Egypt - accounts for a further share, placing "
        "sustained pressure on host communities.", body))
    story.append(Spacer(1, 6))
    story.append(KeepTogether([embed("chart_displacement_trend.png"),
        Paragraph("Figure 1. Displaced population by year, internal vs cross-border "
                  "(illustrative).", caption)]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>2. Drivers of displacement</b>", h2))
    story.append(Paragraph(
        "Armed conflict is the dominant trigger of new displacements, but disaster events - "
        "flooding and drought-linked livelihood failure - drive a rising share each year "
        "(Figure 2). Climate-linked displacement is increasingly entangled with conflict "
        "dynamics: resource pressure and seasonal livelihood loss precede many of the "
        "movements recorded under the conflict heading.", body))
    story.append(Spacer(1, 6))
    story.append(KeepTogether([embed("chart_drivers.png"),
        Paragraph("Figure 2. New internal displacements by trigger, conflict vs disasters "
                  "(illustrative).", caption)]))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>3. Host-country context: Chad</b>", h2))
    story.append(Paragraph("• Over 1.1M refugees and returnees hosted, concentrated in the "
                           "eastern provinces", bullet))
    story.append(Paragraph("• Host communities face pressure on water, grazing land and "
                           "basic services", bullet))
    story.append(Paragraph("• Rains cut access to remote camps for parts of the year",
                           bullet))

    story.append(Paragraph("<b>4. Response & frameworks</b>", h2))
    story.append(Paragraph(
        "The regional refugee response plan and the humanitarian programme cycle set the "
        "current planning figures; the Global Compact for Migration and the Global Compact "
        "on Refugees frame the international response. Links to the primary planning "
        "documents are cited in the annex.", body))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.6, color=BORDER, spaceAfter=6))
    story.append(Paragraph("<b>Sources (annex)</b>", h2))
    for s in [
        "1. UNHCR Population Data Portal, displaced persons relevant to Sudan. "
        "data.unhcr.org  (retrieved Oct 2026 - mockup, illustrative)",
        "2. IDMC Global Internal Displacement Database, conflict & disaster displacements. "
        "internal-displacement.org  (mockup, illustrative)",
        "3. World Bank Open Data, Chad & Sudan population and poverty indicators. "
        "data.worldbank.org  (mockup, illustrative)",
        "4. IOM Displacement Tracking Matrix, Sudan national & cross-border reports. "
        "dtm.iom.int  (mockup, illustrative)",
    ]:
        story.append(Paragraph(s, foot))
    return story


def make_doc(target):
    doc = BaseDocTemplate(
        target, pagesize=A4,
        title="Displacement Snapshot - Sudan (Mockup)", author="Omar Farooq",
        creator="Omar Farooq", subject="Layout mockup with illustrative data",
    )
    first_frame = Frame(MARGIN, BOTTOM, CONTENT_W,
                        PAGE_H - BAND_H - BOTTOM - 0.5 * cm, id="first")
    later_frame = Frame(MARGIN, BOTTOM, CONTENT_W,
                        PAGE_H - TOP_BAND_LATER - BOTTOM - 0.5 * cm, id="later")
    doc.addPageTemplates([
        PageTemplate(id="First", frames=[first_frame], onPage=on_first),
        PageTemplate(id="Later", frames=[later_frame], onPage=on_later),
    ])
    return doc


def count_pages():
    buf = io.BytesIO()
    make_doc(buf).build(make_story())
    return len(pymupdf.open(stream=buf.getvalue(), filetype="pdf"))


if __name__ == "__main__":
    TOTAL_PAGES[0] = count_pages()
    make_doc("mockup_displacement_snapshot.pdf").build(make_story())
    import pymupdf as _pm
    doc = _pm.open("mockup_displacement_snapshot.pdf")
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=110).save("mockup_p%d.png" % i)
    print("pdf done, pages:", TOTAL_PAGES[0])
