"""One function per layout. Each returns an engine.R with ops and truth."""
from reportlab.pdfbase import pdfmetrics
from engine import R, W, H, text_png, photo_png
from content import P1, P2, contact_line

M = 50  # page margin


def _dots(font, size, gap):
    dw = pdfmetrics.stringWidth(" .", font, size)
    return " ." * max(int(gap / dw), 3)


def heading(r, text, x, width, style="normal", rule=True, hs=11.5):
    r.y -= 6
    r.need(30)
    if style == "spaced":
        r.put(text.upper(), x, r.y, size=hs - 0.5, bold=True, cs=3.5, shown=text.upper())
        r.truth[-1] = text
    else:
        r.put(text, x, r.y, size=hs, bold=True)
    r.y -= 4
    if rule:
        r.line(x, r.y, x + width, r.y)
    r.y -= 13


def bullet_lines(r, text, x, width, size, leading, bullet):
    glyph, gfont = bullet
    from reportlab.lib.utils import simpleSplit
    font = r.font
    lines = simpleSplit(text, font, size, width - 14)
    for i, part in enumerate(lines):
        r.need(leading)
        if i == 0 and glyph:
            r.put(glyph, x + 2, r.y, size=size, truth=False, font=gfont)
        r.put(part, x + 14, r.y, size=size)
        r.y -= leading


def experience(r, p, x, width, o, size=10, leading=13.5):
    bullet = o.get("bullet", ("-", None))
    for e in p["experience"]:
        r.need(40)
        r.put(e["role"], x, r.y, size=size + 0.5, bold=True)
        if o.get("leader"):
            role_w = pdfmetrics.stringWidth(e["role"], r.bold, size + 0.5)
            date_w = pdfmetrics.stringWidth(e["dates"], r.font, size)
            gap = width - role_w - date_w - 16
            r.put(_dots(r.font, size, gap), x + role_w + 6, r.y, size=size,
                  truth=False, color=0.5)
        r.put(e["dates"], x + width, r.y, size=size, align="r")
        r.y -= leading
        r.put(e["org"], x, r.y, size=size)
        r.y -= leading
        for b in e["bullets"]:
            bullet_lines(r, b, x, width, size, leading, bullet)
        r.y -= 5


def education(r, p, x, width, size=10, leading=13.5):
    for e in p["education"]:
        r.put(e["degree"], x, r.y, size=size + 0.5, bold=True)
        r.put(e["dates"], x + width, r.y, size=size, align="r")
        r.y -= leading
        r.put(e["school"], x, r.y, size=size)
        r.y -= leading


def contact(r, p, cx, o, y=None):
    y = y if y is not None else r.y
    line = contact_line(p)
    if o.get("link"):
        head = " | ".join([p["city"], p["email"], p["phone"]]) + " | "
        total = pdfmetrics.stringWidth(head + p["link_label"], r.font, 9.5)
        x0 = cx - total / 2
        r.put(head, x0, y, size=9.5, truth=False)
        hw = pdfmetrics.stringWidth(head, r.font, 9.5)
        lw = pdfmetrics.stringWidth(p["link_label"], r.font, 9.5)
        r.put(p["link_label"], x0 + hw, y, size=9.5, truth=False, color=0.25)
        r.line(x0 + hw, y - 1.5, x0 + hw + lw, y - 1.5, width=0.4)
        r.link((x0 + hw, y - 3, x0 + hw + lw, y + 9), p["link_url"])
        r.truth.append(line)
    elif o.get("icons"):
        items = [("⌂", p["city"]), ("✉", p["email"]),
                 ("☎", p["phone"]), ("▶", p["link_label"])]
        widths = [pdfmetrics.stringWidth(i + "  " + t, "DejaVu", 9) + 18
                  for i, t in items]
        x0 = cx - sum(widths) / 2
        for (icon, text), w in zip(items, widths):
            r.put(text, x0, y, size=9, font="DejaVu", shown=icon + "  " + text)
            x0 += w
    else:
        r.put(line, cx, y, size=9.5, align="c")


def header(r, p, o):
    cx = W / 2
    r.group(0)
    if o.get("name_img"):
        data, (iw, ih) = text_png(p["name"], 64)
        h = 26
        w = iw * h / ih
        r.image(data, cx - w / 2, r.y - 6, w, h)
        r.truth.append(p["name"])
    else:
        r.put(p["name"], cx, r.y, size=22, bold=True, align="c")
    r.y -= 20
    r.put(p["title"], cx, r.y, size=12, align="c")
    r.y -= 15
    if not o.get("contact_footer"):
        contact(r, p, cx, o)
        r.y -= 12
    else:
        # contact lives in the footer; truth keeps it after the title
        pass


def body_single(r, p, o, width=W - 2 * M, x=M):
    hs_style = o.get("head_style", "normal")
    size = o.get("size", 10)
    hsz = size + 1.5
    leading = o.get("leading", 13.5)
    r.group(1)
    heading(r, "Summary", x, width, hs_style, hsz)
    r.wrapped(p["summary"], x, width, size=size, leading=leading)
    r.group(2)
    heading(r, "Experience", x, width, hs_style, hsz)
    experience(r, p, x, width, o, size, leading)
    r.group(3)
    heading(r, "Education", x, width, hs_style, hsz)
    education(r, p, x, width, size, leading)
    r.group(4)
    heading(r, "Skills", x, width, hs_style, hsz)
    if o.get("grid"):
        skills_grid(r, p, x, width, size)
    else:
        r.wrapped(", ".join(p["skills"]), x, width, size=size, leading=leading)


def skills_grid(r, p, x, width, size):
    cols, rowh = 3, 20
    cw = width / cols
    rows = [p["skills"][i:i + cols] for i in range(0, len(p["skills"]), cols)]
    top = r.y + 8
    for i, row in enumerate(rows):
        for j, s in enumerate(row):
            r.put(s, x + j * cw + 6, top - i * rowh - 14, size=size)
    n = len(rows)
    for i in range(n + 1):
        r.line(x, top - i * rowh, x + width, top - i * rowh, 0.5)
    for j in range(cols + 1):
        r.line(x + j * cw, top, x + j * cw, top - n * rowh, 0.5)
    r.y = top - n * rowh - 10


def add_page_furniture(r, p):
    """Header and footer text that repeats on every page and is not content."""
    pages = max(o["page"] for o in r.ops) + 1
    saved = r.page
    for pg in range(pages):
        r.page = pg
        r.group_id = 9
        r.put(f"{p['name']} - Curriculum Vitae", M, H - 30, size=8,
              truth=False, color=0.4)
        r.put(f"Page {pg + 1}", W - M, 28, size=8, align="r", truth=False,
              color=0.4)
    r.page = saved


# ------------------------------------------------------------------ layouts

def single(p=P1, **o):
    r = R(font=o.get("font", "Helvetica"), bold=o.get("bold"),
          nfd=o.get("nfd", False), lig=o.get("lig", False))
    header(r, p, o)
    if o.get("contact_footer"):
        pass
    body_single(r, p, o)
    if o.get("contact_footer"):
        # draw contact in the footer but keep it right after the title in truth
        line = contact_line(p)
        idx = 2 if len(r.truth) >= 2 else len(r.truth)
        r.page = 0
        r.group_id = 0
        r.put(line, W / 2, 34, size=9.5, align="c", truth=False)
        r.truth.insert(idx, line)
    if o.get("furniture"):
        add_page_furniture(r, p)
    return r, o.get("group_order")


def two_column_body(p=P1, rows=False):
    r = R()
    r.group(0)
    r.put(p["name"], W / 2, r.y, size=22, bold=True, align="c")
    r.y -= 20
    r.put(p["title"], W / 2, r.y, size=12, align="c")
    r.y -= 15
    r.put(contact_line(p), W / 2, r.y, size=9.5, align="c")
    r.y -= 12
    top = r.y
    cw = (W - 2 * M - 24) / 2
    r.group(2)
    heading(r, "Experience", M, cw)
    experience(r, p, M, cw, {}, size=9.5, leading=12.5)
    r.y, left_end = top, r.y
    x2 = M + cw + 24
    r.group(1)
    heading(r, "Summary", x2, cw)
    r.wrapped(p["summary"], x2, cw, size=9.5, leading=12.5)
    r.group(3)
    heading(r, "Education", x2, cw)
    education(r, p, x2, cw, 9.5, 12.5)
    r.group(4)
    heading(r, "Skills", x2, cw)
    r.wrapped(", ".join(p["skills"]), x2, cw, size=9.5, leading=12.5)
    r.line(M + cw + 12, top + 4, M + cw + 12, 80, 0.4)
    return r, ("rows" if rows else None)


def sidebar(p=P1, photo=False, rows=False):
    r = R()
    sw = 150
    r.group(0)
    r.rect(0, 0, sw + 20, H, fill=0.93, stroke=False)
    r.put(p["name"], 20 + sw + 18, H - 60, size=22, bold=True)
    r.put(p["title"], 20 + sw + 18, H - 80, size=12)
    # sidebar
    y = H - 60
    if photo:
        from engine import photo_png
        r.image(photo_png(), 30, y - 100, 80, 100)
        y -= 120
    r.group(5)
    r.put("Contact", 24, y, size=11.5, bold=True)
    y -= 16
    for s in (p["city"], p["email"], p["phone"], p["link_label"]):
        r.put(s, 24, y, size=9)
        y -= 13
    y -= 10
    r.put("Education", 24, y, size=11.5, bold=True)
    y -= 16
    from reportlab.lib.utils import simpleSplit
    e = p["education"][0]
    for chunk in (e["degree"], e["school"], e["dates"]):
        for part in simpleSplit(chunk, r.font, 9, sw - 6):
            r.put(part, 24, y, size=9)
            y -= 12
    y -= 10
    r.put("Skills", 24, y, size=11.5, bold=True)
    y -= 16
    for s in p["skills"]:
        r.put(s, 24, y, size=9)
        y -= 13
    # main
    x = 20 + sw + 18
    width = W - x - 40
    r.y = H - 110
    r.group(1)
    heading(r, "Summary", x, width)
    r.wrapped(p["summary"], x, width, size=10, leading=13.5)
    r.group(2)
    heading(r, "Experience", x, width)
    experience(r, p, x, width, {})
    return r, ("rows" if rows else None)


def experience_table(p=P1):
    r = R()
    header(r, p, {})
    r.group(1)
    heading(r, "Summary", M, W - 2 * M)
    r.wrapped(p["summary"], M, W - 2 * M)
    r.group(2)
    heading(r, "Experience", M, W - 2 * M)
    dw = 95
    x = M
    width = W - 2 * M
    for e in p["experience"]:
        top = r.y + 10
        r.put(e["dates"], x + 4, r.y, size=10)
        r.put(e["role"], x + dw + 8, r.y, size=10.5, bold=True)
        r.y -= 13.5
        r.put(e["org"], x + dw + 8, r.y, size=10)
        r.y -= 13.5
        for b in e["bullets"]:
            bullet_lines(r, b, x + dw + 8, width - dw - 8, 10, 13.5, ("-", None))
        bottom = r.y + 4
        r.line(x, top, x + width, top, 0.5)
        r.line(x, bottom, x + width, bottom, 0.5)
        r.line(x + dw, top, x + dw, bottom, 0.5)
        r.y -= 12
    r.group(3)
    heading(r, "Education", M, W - 2 * M)
    education(r, p, M, W - 2 * M)
    r.group(4)
    heading(r, "Skills", M, W - 2 * M)
    r.wrapped(", ".join(p["skills"]), M, W - 2 * M)
    return r, None
