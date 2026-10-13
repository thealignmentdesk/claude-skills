#!/usr/bin/env python3
"""Turn a workbook plan (JSON) into two printable PDFs: the student workbook and a separate answer key.

    python3 scripts/make_workbook.py workbook.json [out_dir]
      -> <out_dir>/<slug>-workbook.pdf and <slug>-answer-key.pdf

Needs reportlab (pip install reportlab). The JSON format is in references/workbook-json.md.
"""
import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, Flowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

INK = colors.HexColor("#1c1b19")
ACC = colors.HexColor("#c96442")
SOFT = colors.HexColor("#f4efe6")
LINE = colors.HexColor("#c4bcae")
MUTE = colors.HexColor("#6e6a63")
PRINTER = False   # printer friendly: no tinted boxes, black accents (set from the plan)
LEVELS = {1: "Warm-up", 2: "Practice", 3: "Challenge"}


def pick_fonts():
    """A font with ×, ÷, √, π, ≤, ≥, fractions and accents; Helvetica if none is found."""
    pairs = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf"),
        ("/Library/Fonts/Arial Unicode.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ]
    for reg, bold in pairs:
        if os.path.exists(reg) and os.path.exists(bold):
            pdfmetrics.registerFont(TTFont("WB", reg))
            pdfmetrics.registerFont(TTFont("WB-Bold", bold))
            return "WB", "WB-Bold"
    return "Helvetica", "Helvetica-Bold"


FONT, BOLD = "Helvetica", "Helvetica-Bold"   # chosen per workbook in build()


def styles(young):
    base = 15 if young else 11.5   # bigger print for grades 1-3
    s = {
        "title": ParagraphStyle("title", fontName=BOLD, fontSize=30, leading=36, textColor=INK, alignment=TA_CENTER),
        "sub": ParagraphStyle("sub", fontName=FONT, fontSize=15, leading=20, textColor=ACC, alignment=TA_CENTER),
        "h": ParagraphStyle("h", fontName=BOLD, fontSize=base + 6, leading=base + 10, textColor=ACC, spaceBefore=4, spaceAfter=6),
        "body": ParagraphStyle("body", fontName=FONT, fontSize=base, leading=base * 1.45, textColor=INK),
        "small": ParagraphStyle("small", fontName=FONT, fontSize=base - 2.5, leading=(base - 2.5) * 1.4, textColor=MUTE),
        "q": ParagraphStyle("q", fontName=FONT, fontSize=base, leading=base * 1.5, textColor=INK),
        "level": ParagraphStyle("level", fontName=BOLD, fontSize=base - 1, leading=base + 4, textColor=MUTE, spaceBefore=8),
    }
    return s


def esc(text):
    """Plain text to reportlab paragraph markup; **bold** allowed."""
    t = str(text)
    if FONT == "Helvetica":
        t = t.replace("−", "-")   # math minus: not in the built-in font, a hyphen prints the same
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", rf'<font name="{BOLD}">\1</font>', t)
    return t.replace("\n", "<br/>")


class Lines(Flowable):
    """Ruled writing lines (or an empty box for working out)."""
    def __init__(self, n, width, gap, box=False):
        super().__init__()
        self.n, self.width, self.gap, self.box = n, width, gap, box
        self.height = n * gap + 4

    def draw(self):
        c = self.canv
        c.setStrokeColor(LINE)
        if self.box:
            c.setLineWidth(1)
            c.roundRect(0, 0, self.width, self.height - 2, 6)
            return
        c.setLineWidth(0.7)
        for k in range(1, self.n + 1):
            y = self.height - k * self.gap
            c.line(0, y, self.width, y)


class NumberLine(Flowable):
    def __init__(self, start, end, step, width, label_every=1):
        super().__init__()
        self.start, self.end, self.step, self.width, self.every = start, end, step, width, label_every
        self.height = 34

    def draw(self):
        c = self.canv
        n = int(round((self.end - self.start) / self.step))
        c.setStrokeColor(INK)
        c.setLineWidth(1.2)
        c.line(4, 20, self.width - 4, 20)
        c.setFont(FONT, 9)
        for k in range(n + 1):
            x = 4 + (self.width - 8) * k / max(n, 1)
            c.line(x, 15, x, 25)
            if k % self.every == 0:
                v = self.start + k * self.step
                c.drawCentredString(x, 3, f"{v:g}")


def boxed(flowables, width, fill=None, border=None):
    fill = SOFT if fill is None else fill
    if PRINTER and border is None:
        border = LINE
    t = Table([[flowables]], colWidths=[width])
    st = [("BACKGROUND", (0, 0), (-1, -1), fill), ("LEFTPADDING", (0, 0), (-1, -1), 10),
          ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]
    if border:
        st.append(("BOX", (0, 0), (-1, -1), 1.2, border))
    t.setStyle(TableStyle(st))
    return t


def question_block(num, q, st, width, young):
    parts = [Paragraph(f'<font name="{BOLD}">{num}.</font>&nbsp;&nbsp;{esc(q["q"])}', st["q"])]
    kind = q.get("type", "short")
    if q.get("number_line"):
        nl = q["number_line"]
        parts.append(Spacer(1, 4))
        parts.append(NumberLine(nl["from"], nl["to"], nl.get("step", 1), width - 20, nl.get("label_every", 1)))
    if kind == "mc":
        mark = "( )" if FONT == "Helvetica" else "○"
        rows = [[Paragraph(f"{mark}&nbsp;&nbsp;{chr(65 + i)}.&nbsp;&nbsp;{esc(ch)}", st["q"])] for i, ch in enumerate(q.get("choices", []))]
        parts.append(Table(rows, colWidths=[width - 30], style=[("LEFTPADDING", (0, 0), (-1, -1), 18),
                                                                ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    elif kind == "fill":
        pass   # blanks are written into the question as ____
    else:
        n = q.get("lines", {"short": 1, "long": 4, "work": 5}.get(kind, 2))
        gap = 30 if young else 22
        parts.append(Spacer(1, 4))
        parts.append(Lines(n, width - 10, gap, box=(kind == "work")))
    parts.append(Spacer(1, 10 if young else 8))
    return KeepTogether(parts)


def footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(FONT, 8)
        canvas.setFillColor(MUTE)
        canvas.drawString(doc.leftMargin, 10 * mm, text)
        canvas.drawRightString(doc.pagesize[0] - doc.rightMargin, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


def build(plan, out_dir):
    global ACC, SOFT, LINE, PRINTER, FONT, BOLD
    try:   # plain Latin text: use the PDF's built-in Helvetica, no embedded font, so the file is ~5x smaller (easier to email)
        json.dumps(plan, ensure_ascii=False).replace("−", "-").encode("cp1252")   # Helvetica's WinAnsi set
        FONT, BOLD = "Helvetica", "Helvetica-Bold"
    except UnicodeEncodeError:
        FONT, BOLD = pick_fonts()
    if plan.get("printer_friendly"):
        PRINTER, ACC, SOFT, LINE = True, INK, colors.white, colors.HexColor("#8a8a8a")
    young = int(re.sub(r"\D", "", str(plan.get("grade", "5"))) or 5) <= 3
    st = styles(young)
    size = A4 if plan.get("paper", "letter").lower() == "a4" else LETTER
    slug = re.sub(r"[^a-z0-9]+", "-", plan["title"].lower()).strip("-")[:60]
    os.makedirs(out_dir, exist_ok=True)
    margin = 18 * mm
    width = size[0] - 2 * margin
    foot = f'{plan.get("grade", "")} {plan.get("subject", "")} · {plan.get("region", "")}'.strip()

    # ---- student workbook
    name_line = f'Name: {esc(plan["child"])}' if plan.get("child") else "Name: ______________________________"
    cur = plan.get("curriculum", {})
    if plan.get("compact_cover"):   # a header on page 1 instead of a cover page (saves a page)
        story = [Paragraph(esc(plan["title"]), st["h"]),
                 Paragraph(esc(f'{plan.get("grade", "")} · {plan.get("subject", "")}' + (f' · Follows: {cur.get("name", "")}' if cur else "")), st["small"]),
                 Spacer(1, 4),
                 Table([[Paragraph(name_line, st["body"]), Paragraph("Date: ________________", st["body"])]],
                       colWidths=[width * 0.62, width * 0.38]),
                 Spacer(1, 10)]
    else:
        story = [Spacer(1, 40 * mm), Paragraph(esc(plan["title"]), st["title"]), Spacer(1, 6),
                 Paragraph(esc(f'{plan.get("grade", "")} · {plan.get("subject", "")}'), st["sub"]), Spacer(1, 18 * mm)]
        story.append(Table([[Paragraph(name_line, st["body"]),
                             Paragraph("Date: ________________", st["body"])]], colWidths=[width * 0.62, width * 0.38]))
        story.append(Spacer(1, 14 * mm))
        toc = [Paragraph(f'<font name="{BOLD}">Inside</font>', st["body"])]
        for i, sec in enumerate(plan["sections"], 1):
            toc.append(Paragraph(f'{i}. {esc(sec["heading"])}', st["body"]))
        story.append(boxed(toc, width))
        story.append(Spacer(1, 8 * mm))
        if cur:
            story.append(Paragraph(esc(f'Follows: {cur.get("name", "")}') + (f'<br/>{esc(cur["url"])}' if cur.get("url") else ""), st["small"]))
        if plan.get("for_adults"):
            story.append(Spacer(1, 4 * mm))
            story.append(Paragraph(f'<font name="{BOLD}">For the adult:</font> {esc(plan["for_adults"])}', st["small"]))
        story.append(PageBreak())

    num = 0
    for i, sec in enumerate(plan["sections"], 1):
        if i > 1:
            story.append(CondPageBreak(60 * mm))
        story.append(Paragraph(f'{i}. {esc(sec["heading"])}', st["h"]))
        if sec.get("expectation"):
            e = sec["expectation"]
            code = f'<font name="{BOLD}">{esc(e.get("code", ""))}</font> ' if e.get("code") else ""
            story.append(Paragraph(f'Curriculum: {code}{esc(e.get("text", ""))}', st["small"]))
            story.append(Spacer(1, 6))
        if sec.get("remember"):
            story.append(boxed([Paragraph(f'<font name="{BOLD}">Remember</font>', st["body"])] +
                               [Paragraph(f"•&nbsp;&nbsp;{esc(r)}", st["body"]) for r in sec["remember"]], width))
            story.append(Spacer(1, 8))
        if sec.get("example"):
            ex = sec["example"]
            items = [Paragraph(f'<font name="{BOLD}">Example:</font> {esc(ex["q"])}', st["body"])]
            items += [Paragraph(f"{k}.&nbsp;&nbsp;{esc(s)}", st["body"]) for k, s in enumerate(ex.get("steps", []), 1)]
            if ex.get("answer"):
                items.append(Paragraph(f'<font name="{BOLD}">Answer:</font> {esc(ex["answer"])}', st["body"]))
            story.append(boxed(items, width, fill=colors.white, border=ACC))
            story.append(Spacer(1, 10))
        last_level = None
        for q in sec["questions"]:
            num += 1
            q["_num"] = num
            lvl = q.get("level")
            block = question_block(num, q, st, width, young)
            if lvl and lvl != last_level:
                block = KeepTogether([Paragraph(LEVELS.get(lvl, ""), st["level"])] + block._content)
                last_level = lvl
            story.append(block)
    doc = SimpleDocTemplate(os.path.join(out_dir, f"{slug}-workbook.pdf"), pagesize=size, leftMargin=margin,
                            rightMargin=margin, topMargin=margin, bottomMargin=20 * mm, title=plan["title"])
    doc.build(story, onFirstPage=footer(foot), onLaterPages=footer(foot))
    pages = doc.page

    # ---- answer key (separate file, so the child can't see it)
    key = [Paragraph(esc(f'Answer key: {plan["title"]}'), st["h"]),
           Paragraph("For the parent or teacher. Keep this separate from the workbook.", st["small"]), Spacer(1, 8)]
    if plan.get("from_scan"):
        fs = plan["from_scan"]
        notes = [Paragraph(f'<font name="{BOLD}">Built from the scanned page</font>', st["body"])]
        notes += [Paragraph(f"•&nbsp;&nbsp;{esc(n)}", st["body"]) for n in fs.get("notes", [])]
        key += [boxed(notes, width), Spacer(1, 10)]
    for i, sec in enumerate(plan["sections"], 1):
        key.append(Paragraph(f'{i}. {esc(sec["heading"])}', st["body"]))
        rows = []
        for q in sec["questions"]:
            ans = f'<font name="{BOLD}">{esc(q.get("answer", ""))}</font>'
            if q.get("explain"):
                ans += f'<br/><font color="#6e6a63">{esc(q["explain"])}</font>'
            rows.append([Paragraph(f'{q["_num"]}.', st["body"]), Paragraph(ans, st["body"])])
        t = Table(rows, colWidths=[12 * mm, width - 12 * mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        key += [t, Spacer(1, 10)]
    if cur:
        key.append(Paragraph(esc(f'Curriculum source: {cur.get("name", "")} {cur.get("url", "")}'), st["small"]))
    doc = SimpleDocTemplate(os.path.join(out_dir, f"{slug}-answer-key.pdf"), pagesize=size, leftMargin=margin,
                            rightMargin=margin, topMargin=margin, bottomMargin=20 * mm, title=f'Answer key: {plan["title"]}')
    doc.build(key, onFirstPage=footer(foot + " · answer key"), onLaterPages=footer(foot + " · answer key"))
    print(f"workbook pages: {pages}", file=sys.stderr)
    return [os.path.join(out_dir, f"{slug}-workbook.pdf"), os.path.join(out_dir, f"{slug}-answer-key.pdf")]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        plan = json.load(f)
    for p in build(plan, sys.argv[2] if len(sys.argv) > 2 else "."):
        print(p)
