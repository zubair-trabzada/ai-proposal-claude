#!/usr/bin/env python3
"""
AI Agency Proposal Builder — Professional PDF Generator

Renders a client-ready proposal PDF from a PROPOSAL-*.md markdown file.
Parses headers, paragraphs, tables, and bullet lists into a polished,
branded document with a cover page.

Usage:
  python3 generate_proposal_pdf.py PROPOSAL-Acme.md
  python3 generate_proposal_pdf.py PROPOSAL-Acme.md OUTPUT.pdf
  python3 generate_proposal_pdf.py --demo            # sample proposal

Requires: reportlab>=4.0.0  (pip install reportlab)
"""

import sys
import os
import re
from datetime import datetime, timedelta

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak, KeepTogether, ListFlowable,
                                     ListItem)
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette — Professional Agency Theme (Deep Indigo + Teal + Gold)
# ---------------------------------------------------------------------------
COLORS = {
    "indigo":      HexColor("#1e293b"),   # primary dark
    "indigo_dark": HexColor("#0f172a"),
    "accent":      HexColor("#0ea5e9"),   # sky/teal accent
    "accent_dark": HexColor("#0369a1"),
    "gold":        HexColor("#eab308"),   # highlight / recommended
    "gold_light":  HexColor("#fef9c3"),
    "green":       HexColor("#10b981"),
    "red":         HexColor("#ef4444"),
    "gray":        HexColor("#64748b"),
    "light_bg":    HexColor("#f1f5f9"),
    "row_alt":     HexColor("#f8fafc"),
    "text":        HexColor("#1f2937"),
    "text_light":  HexColor("#64748b"),
    "border":      HexColor("#e2e8f0"),
    "white":       white,
    "black":       black,
}


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def get_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle("CoverTitle", parent=base["Title"],
            fontSize=30, textColor=COLORS["white"], leading=36,
            fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=8),
        "cover_sub": ParagraphStyle("CoverSub", parent=base["Normal"],
            fontSize=14, textColor=COLORS["accent"], leading=18,
            fontName="Helvetica-Bold", alignment=TA_LEFT, spaceAfter=4),
        "cover_meta": ParagraphStyle("CoverMeta", parent=base["Normal"],
            fontSize=11, textColor=COLORS["white"], leading=16,
            fontName="Helvetica", alignment=TA_LEFT),
        "h1": ParagraphStyle("H1", parent=base["Heading1"],
            fontSize=19, textColor=COLORS["indigo"], spaceBefore=16, spaceAfter=8,
            fontName="Helvetica-Bold", leading=23),
        "h2": ParagraphStyle("H2", parent=base["Heading2"],
            fontSize=14, textColor=COLORS["accent_dark"], spaceBefore=12, spaceAfter=5,
            fontName="Helvetica-Bold", leading=18),
        "h3": ParagraphStyle("H3", parent=base["Heading3"],
            fontSize=11.5, textColor=COLORS["indigo"], spaceBefore=8, spaceAfter=3,
            fontName="Helvetica-Bold", leading=15),
        "body": ParagraphStyle("Body", parent=base["Normal"],
            fontSize=10, textColor=COLORS["text"], spaceAfter=6,
            fontName="Helvetica", leading=14.5),
        "bullet": ParagraphStyle("Bullet", parent=base["Normal"],
            fontSize=10, textColor=COLORS["text"], spaceAfter=3,
            fontName="Helvetica", leading=14, leftIndent=6),
        "cell": ParagraphStyle("Cell", parent=base["Normal"],
            fontSize=9, textColor=COLORS["text"], fontName="Helvetica", leading=12),
        "cell_bold": ParagraphStyle("CellBold", parent=base["Normal"],
            fontSize=9, textColor=COLORS["indigo"], fontName="Helvetica-Bold", leading=12),
        "cell_head": ParagraphStyle("CellHead", parent=base["Normal"],
            fontSize=9.5, textColor=COLORS["white"], fontName="Helvetica-Bold", leading=12),
        "disclaimer": ParagraphStyle("Disc", parent=base["Normal"],
            fontSize=7.5, textColor=COLORS["text_light"], fontName="Helvetica-Oblique",
            leading=10, spaceBefore=4),
    }


# ---------------------------------------------------------------------------
# Inline markdown (bold) -> reportlab markup
# ---------------------------------------------------------------------------
def inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r"<font face='Courier'>\1</font>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r"<u>\1</u>", text)
    text = text.replace("★", "&#9733;")
    return text


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------
def parse_markdown(md):
    """Parse markdown into a list of block tuples."""
    blocks = []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+$", line.strip()):
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            blocks.append(("h%d" % min(level, 3), m.group(2).strip()))
            i += 1
            continue

        # Table
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i+1]):
            table_lines = [line]
            i += 1  # header
            i += 1  # separator
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i].rstrip())
                i += 1
            blocks.append(("table", table_lines))
            continue

        # Bullet list
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i].rstrip()))
                i += 1
            blocks.append(("ul", items))
            continue

        # Numbered list
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i].rstrip()))
                i += 1
            blocks.append(("ol", items))
            continue

        # Paragraph (gather consecutive non-empty, non-special lines)
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|---+$)", lines[i]) and "|" not in lines[i]:
            para.append(lines[i].rstrip())
            i += 1
        blocks.append(("p", " ".join(para)))

    return blocks


def split_table_row(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def build_table(table_lines, styles):
    rows = [split_table_row(r) for r in table_lines]
    header = rows[0]
    body = rows[1:]
    ncols = len(header)

    # Detect a "recommended" column (contains ★) for gold highlight
    rec_col = None
    for ci, h in enumerate(header):
        if "★" in h or "RECOMMENDED" in h.upper():
            rec_col = ci

    data = []
    data.append([Paragraph(inline(c), styles["cell_head"]) for c in header])
    for r in body:
        while len(r) < ncols:
            r.append("")
        cells = []
        for ci, c in enumerate(r):
            st = styles["cell_bold"] if ci == 0 else styles["cell"]
            cells.append(Paragraph(inline(c), st))
        data.append(cells)

    avail = 7.0 * inch
    col_widths = [avail / ncols] * ncols

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["indigo"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, COLORS["border"]),
    ]
    for ri in range(1, len(data)):
        if ri % 2 == 0:
            style.append(("BACKGROUND", (0, ri), (-1, ri), COLORS["row_alt"]))
    if rec_col is not None:
        style.append(("BACKGROUND", (rec_col, 0), (rec_col, -1), COLORS["gold_light"]))
        style.append(("BACKGROUND", (rec_col, 0), (rec_col, 0), COLORS["gold"]))
        style.append(("BOX", (rec_col, 0), (rec_col, -1), 1.2, COLORS["gold"]))
    t.setStyle(TableStyle(style))
    return t


# ---------------------------------------------------------------------------
# Cover page
# ---------------------------------------------------------------------------
def wrap_words(text, max_chars):
    """Wrap text onto lines no longer than max_chars, breaking on spaces."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


def make_cover(meta, styles):
    elems = []
    w = 7.5 * inch
    band = Drawing(w, 230)
    band.add(Rect(0, 0, w, 230, fillColor=COLORS["indigo_dark"], strokeColor=None))
    band.add(Rect(0, 0, 6, 230, fillColor=COLORS["accent"], strokeColor=None))
    band.add(Rect(0, 222, w, 8, fillColor=COLORS["accent"], strokeColor=None))
    band.add(String(28, 175, "PROPOSAL", fontSize=13, fillColor=COLORS["accent"],
                    fontName="Helvetica-Bold"))
    title = meta.get("title", "Engagement Proposal")
    # wrap title on word boundaries (~34 chars per line at 24pt)
    title_lines = wrap_words(title, 34)[:2]
    ty = 140
    for tl in title_lines:
        band.add(String(28, ty, tl, fontSize=24, fillColor=COLORS["white"],
                        fontName="Helvetica-Bold"))
        ty -= 28
    band.add(String(28, 78, ("Prepared for: %s" % meta.get("client", ""))[:60],
                    fontSize=12, fillColor=COLORS["white"], fontName="Helvetica"))
    band.add(String(28, 58, ("Prepared by: %s" % meta.get("agency", "[YOUR AGENCY]"))[:60],
                    fontSize=11, fillColor=HexColor("#cbd5e1"), fontName="Helvetica"))
    band.add(String(28, 34, ("Date: %s" % meta.get("date", ""))[:60],
                    fontSize=10, fillColor=HexColor("#cbd5e1"), fontName="Helvetica"))
    band.add(String(28, 18, ("Valid until: %s" % meta.get("valid", ""))[:60],
                    fontSize=10, fillColor=HexColor("#cbd5e1"), fontName="Helvetica"))
    elems.append(band)
    elems.append(Spacer(1, 18))
    return elems


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(COLORS["border"])
    canvas.setLineWidth(0.5)
    canvas.line(0.9 * inch, 0.6 * inch, 7.6 * inch, 0.6 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(COLORS["text_light"])
    canvas.drawString(0.9 * inch, 0.42 * inch, "CONFIDENTIAL")
    canvas.drawRightString(7.6 * inch, 0.42 * inch, "Page %d" % doc.page)
    canvas.drawCentredString(4.25 * inch, 0.42 * inch, "Generated by AI Agency Proposal Builder")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------
def render(md, out_path, meta):
    styles = get_styles()
    doc = SimpleDocTemplate(out_path, pagesize=letter,
        leftMargin=0.9 * inch, rightMargin=0.9 * inch,
        topMargin=0.7 * inch, bottomMargin=0.8 * inch,
        title=meta.get("title", "Proposal"))

    story = []
    story.extend(make_cover(meta, styles))

    blocks = parse_markdown(md)

    # Skip a leading H1 that duplicates the cover title
    skip_first_h1 = True
    for kind, payload in blocks:
        if kind == "h1":
            if skip_first_h1:
                skip_first_h1 = False
                continue
            story.append(Paragraph(inline(payload), styles["h1"]))
        elif kind == "h2":
            story.append(Paragraph(inline(payload), styles["h2"]))
        elif kind == "h3":
            story.append(Paragraph(inline(payload), styles["h3"]))
        elif kind == "p":
            # Skip the metadata block that's already rendered on the cover
            if re.match(r"^\**\s*(Prepared for|Prepared by|Date|Valid Until|CONFIDENTIAL)\b",
                        payload, re.IGNORECASE):
                continue
            story.append(Paragraph(inline(payload), styles["body"]))
        elif kind == "ul":
            items = [ListItem(Paragraph(inline(it), styles["bullet"]), leftIndent=14,
                              value="circle") for it in payload]
            story.append(ListFlowable(items, bulletType="bullet", start="circle",
                                      leftIndent=12))
            story.append(Spacer(1, 4))
        elif kind == "ol":
            items = [ListItem(Paragraph(inline(it), styles["bullet"]), leftIndent=14)
                     for it in payload]
            story.append(ListFlowable(items, bulletType="1", leftIndent=12))
            story.append(Spacer(1, 4))
        elif kind == "table":
            story.append(Spacer(1, 4))
            story.append(build_table(payload, styles))
            story.append(Spacer(1, 8))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "This proposal is confidential and intended solely for the named recipient. "
        "Pricing and availability are valid until the date shown on the cover.",
        styles["disclaimer"]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("PDF written to: %s" % out_path)


# ---------------------------------------------------------------------------
# Metadata extraction from the markdown
# ---------------------------------------------------------------------------
def extract_meta(md, src_name):
    meta = {}
    # Title: first H1
    m = re.search(r"^#\s+(.*)$", md, re.MULTILINE)
    meta["title"] = (m.group(1).strip() if m else "Engagement Proposal").replace("Proposal:", "").strip()

    def find(label):
        mm = re.search(r"(?im)^\**\s*%s\**\s*[:\-]\s*(.+)$" % re.escape(label), md)
        return mm.group(1).strip().strip("*") if mm else None

    meta["client"] = find("Prepared for") or find("Client") or "[CLIENT]"
    meta["agency"] = find("Prepared by") or find("Agency") or "[YOUR AGENCY]"
    meta["date"] = find("Date") or datetime.now().strftime("%B %d, %Y")
    meta["valid"] = find("Valid Until") or find("Valid until") or \
        (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")
    # clean client of any "[Title]" trailing markup
    meta["client"] = re.sub(r",?\s*\[.*?\]", "", meta["client"]).strip() or "[CLIENT]"
    return meta


DEMO_MD = """# Proposal: AI Search Visibility Strategy for Example Agency

Prepared for: Example Agency
Prepared by: [YOUR AGENCY]
Date: __DATE__
Valid Until: __VALID__

## Executive Summary

Example Agency has built a strong reputation offline, but in the AI search era that
reputation is invisible. Our GEO audit scored your site **52/100 (Grade C)** — meaning
when prospects ask ChatGPT, Perplexity, or Google's AI for a firm like yours, you are
rarely the answer. AI-referred traffic is growing **527% year over year**, and your
competitors are already being cited. This proposal lays out a 90-day plan to close that
gap and turn AI search into a predictable lead source.

## Situation Analysis

### Current State
Your site scored 52/100 overall, dragged down by three weak categories from the audit.

| Category | Score | Status |
|----------|-------|--------|
| Schema Markup | 30/100 | Critical |
| Trust Signals | 45/100 | Weak |
| AI Readiness | 55/100 | Mixed |
| Content Quality | 75/100 | Strong |
| Technical SEO | 85/100 | Strong |

### Opportunities Identified
- Add FAQPage and Organization schema to become machine-readable to AI crawlers
- Publish an llms.txt file so AI systems can map your services
- Restructure top pages into answer-first passages AI can quote directly

## Investment

| | Audit | Growth ★ RECOMMENDED | Dominate |
|---|---|---|---|
| Price | $1,500 one-time | $3,500/mo | $7,000/mo |
| GEO audit & fixes | Yes | Yes | Yes |
| Monthly re-scoring | No | Yes | Yes |
| Content production | No | 4 pages/mo | 10 pages/mo |
| Competitor tracking | No | Yes | Yes |
| Expected 12-mo ROI | 3x | 6x | 9x |

## Next Steps

1. Review this proposal and share with your team
2. Book a 30-minute walkthrough call
3. Sign via e-signature and we begin within one week

[YOUR NAME] — [YOUR EMAIL] — [YOUR AGENCY]
"""
DEMO_MD = (DEMO_MD
           .replace("__DATE__", datetime.now().strftime("%B %d, %Y"))
           .replace("__VALID__", (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")))


def main():
    args = [a for a in sys.argv[1:]]
    if not args or args[0] == "--demo":
        md = DEMO_MD
        src = "PROPOSAL-demo.md"
        out = "PROPOSAL-sample.pdf"
    else:
        src = args[0]
        if not os.path.exists(src):
            print("Error: file not found: %s" % src)
            sys.exit(1)
        with open(src, "r", encoding="utf-8") as f:
            md = f.read()
        if len(args) > 1:
            out = args[1]
        else:
            base = os.path.splitext(os.path.basename(src))[0]
            out = base + ".pdf"

    meta = extract_meta(md, src)
    render(md, out, meta)


if __name__ == "__main__":
    main()
