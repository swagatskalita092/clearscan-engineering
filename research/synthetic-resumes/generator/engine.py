"""A tiny layout engine on top of reportlab.

Every text item is recorded twice: once as a drawing operation (where it goes
on the page, in what order it is written into the file) and once as ground
truth (what a human reads, in reading order). Layouts can make the two orders
differ on purpose.
"""
import io
import unicodedata
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.utils import simpleSplit
from PIL import Image, ImageDraw, ImageFont

W, H = A4
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", DEJAVU))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", DEJAVU_B))
from reportlab.pdfbase.cidfonts import UnicodeCIDFont  # noqa: E402
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

LIGS = (("ffi", "ﬃ"), ("fi", "ﬁ"), ("fl", "ﬂ"))


def ligate(s):
    for a, b in LIGS:
        s = s.replace(a, b)
    return s


class R:
    """Records operations for one document."""

    def __init__(self, font="Helvetica", bold=None, nfd=False, lig=False):
        self.font = font
        self.bold = bold or (font + "-Bold")
        self.nfd = nfd
        self.lig = lig
        self.ops = []
        self.truth = []          # reading-order strings
        self.links = []          # (page, rect, url)
        self.group_id = 0
        self.page = 0
        self.y = H - 60
        self.on_newpage = None
        self.bottom = 60

    # --- text ---
    def put(self, s, x, y, size=10, bold=False, align="l", cs=0, truth=True,
            font=None, color=0, shown=None):
        drawn = shown if shown is not None else s
        if self.lig:
            drawn = ligate(drawn)
        if self.nfd:
            drawn = unicodedata.normalize("NFD", drawn)
        f = font or (self.bold if bold else self.font)
        self.ops.append(dict(kind="text", s=drawn, x=x, y=y, size=size, f=f,
                             align=align, cs=cs, page=self.page,
                             group=self.group_id, color=color))
        if truth:
            self.truth.append(s)

    def image(self, data, x, y, w, h):
        self.ops.append(dict(kind="img", data=data, x=x, y=y, w=w, h=h,
                             page=self.page, group=self.group_id))

    def link(self, rect, url):
        self.links.append((self.page, rect, url))

    def line(self, x1, y1, x2, y2, width=0.6):
        self.ops.append(dict(kind="line", x1=x1, y1=y1, x2=x2, y2=y2,
                             width=width, page=self.page, group=self.group_id))

    def rect(self, x, y, w, h, fill=None, stroke=True):
        self.ops.append(dict(kind="rect", x=x, y=y, w=w, h=h, fill=fill,
                             stroke=stroke, page=self.page, group=self.group_id))

    def group(self, n):
        self.group_id = n

    # --- flow ---
    def newpage(self):
        self.page += 1
        self.y = H - 60
        if self.on_newpage:
            self.on_newpage(self)

    def need(self, h):
        if self.y - h < self.bottom:
            self.newpage()

    def wrapped(self, s, x, width, size=10, bold=False, leading=None,
                truth=True):
        font = self.bold if bold else self.font
        leading = leading or size * 1.35
        for part in simpleSplit(s, font, size, width):
            self.need(leading)
            self.put(part, x, self.y, size=size, bold=bold, truth=truth)
            self.y -= leading

    # --- output ---
    def save(self, path, group_order=None):
        c = canvas.Canvas(str(path), pagesize=A4, invariant=1)
        c.setTitle("Synthetic resume")
        c.setAuthor("clearscan-engineering")
        pages = max(o["page"] for o in self.ops) + 1
        for pg in range(pages):
            ops = [o for o in self.ops if o["page"] == pg]
            if group_order == "rows":
                other = [o for o in ops if o["kind"] != "text"]
                texts = sorted((o for o in ops if o["kind"] == "text"),
                               key=lambda o: (-round(o["y"]), o["x"]))
                ops = other + texts
            elif group_order:
                rank = {g: i for i, g in enumerate(group_order)}
                ops.sort(key=lambda o: rank.get(o["group"], 99))
            for o in ops:
                self._draw(c, o)
            for (lp, rect, url) in self.links:
                if lp == pg:
                    c.linkURL(url, rect, relative=0)
            c.showPage()
        c.save()

    def _draw(self, c, o):
        k = o["kind"]
        if k == "text":
            c.setFillGray(o["color"])
            c.setFont(o["f"], o["size"])
            s, x, y, cs = o["s"], o["x"], o["y"], o["cs"]
            width = pdfmetrics.stringWidth(s, o["f"], o["size"]) + cs * len(s)
            if o["align"] == "r":
                x = x - width
            elif o["align"] == "c":
                x = x - width / 2
            if cs:
                c.saveState()
                t = c.beginText(x, y)
                t.setFont(o["f"], o["size"])
                t.setCharSpace(cs)
                t.textOut(s)
                c.drawText(t)
                c.restoreState()
            else:
                c.drawString(x, y, s)
            c.setFillGray(0)
        elif k == "img":
            c.drawImage(ImageReader(io.BytesIO(o["data"])), o["x"], o["y"],
                        o["w"], o["h"], mask="auto")
        elif k == "line":
            c.setLineWidth(o["width"])
            c.line(o["x1"], o["y1"], o["x2"], o["y2"])
        elif k == "rect":
            if o["fill"] is not None:
                c.setFillGray(o["fill"])
            c.rect(o["x"], o["y"], o["w"], o["h"], stroke=int(o["stroke"]),
                   fill=int(o["fill"] is not None))
            c.setFillGray(0)


def text_png(text, size=64):
    """Render text to a PNG so that a name exists only as pixels."""
    f = ImageFont.truetype(DEJAVU_B, size)
    tmp = Image.new("L", (10, 10), 255)
    d = ImageDraw.Draw(tmp)
    box = d.textbbox((0, 0), text, font=f)
    img = Image.new("L", (box[2] + 20, box[3] + 20), 255)
    ImageDraw.Draw(img).text((10, 6), text, font=f, fill=0)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue(), img.size


def photo_png():
    """A neutral grey silhouette used as a stand-in portrait."""
    img = Image.new("RGB", (240, 300), (205, 208, 214))
    d = ImageDraw.Draw(img)
    d.ellipse((80, 50, 160, 130), fill=(150, 154, 163))
    d.ellipse((40, 150, 200, 360), fill=(150, 154, 163))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()
