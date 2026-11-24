#!/usr/bin/env python3
"""Meme A (v6) — the ORIGINAL "MUTED" chat meme, new background, small robot,
text & layout round.

The user asked: like the first one, just change the background (v4) — then
add a small robot (v5) — then fix the text & layout (v6). Same chat window,
same bubble structure, same wording exactly:
  human: "hey, can you just mute the group chat for the weekend?"
  agent: "Done." / "I muted your landlord, your mum, and the wedding group."
         / "I also left the group." / "Goodbye."
  system: "AGENT has left the chat"
  caption strip: "it was only supposed to mute notifications"

v6 changes are typography/layout ONLY (background, robots, wording untouched):
  - the punchline bubble is now bold + larger, with a clean two-line break
    ("I muted your landlord, your mum," / "and the wedding group.") so the
    key phrase is no longer orphaned on its own line;
  - the human bubble breaks as "hey, can you just mute the" /
    "group chat for the weekend?" instead of dangling "the weekend?";
  - bubble type is slightly larger overall (30 -> 32pt) and the pause after
    "Done." is longer, so the punchline lands as the visual peak and the
    chat fills the card instead of leaving a dead band at the bottom;
  - header "AGENT"/"online" spacing eased; caption pill type 30 -> 32pt.

Background: deep navy-to-indigo vertical gradient with a soft glow behind
the chat window, a faint dot grid, and two oversized ghost chat bubbles in
the corners. Robot (v5): the header avatar "A" is now a small smug robot
face (it IS the agent), and one tiny robot waves goodbye from the
bottom-right corner — both small accents, the chat stays the focus.
1024x1024, deterministic (no randomness, no timestamps), PIL only."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NOTO_BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
NOTO_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
NOTO_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

# ---- background palette: deep navy -> indigo ----
BG_TOP = (13, 24, 58)
BG_BOTTOM = (46, 45, 118)
GLOW = (96, 110, 220)
WHITE = (255, 255, 255)
CARD = (250, 250, 252)       # chat card
CARD_HEAD = (23, 37, 84)     # chat header bar
INK = (30, 41, 59)           # agent bubble text
HUMAN_BLUE = (30, 120, 200)  # human bubble
AGENT_GREY = (232, 236, 240)  # agent bubble
SYS_GREY = (90, 100, 115)    # system line text
SYS_PILL = (226, 230, 236)   # system line pill
TEAL = (0, 150, 136)         # avatar
GREEN = (140, 230, 180)      # "online"
RED = (196, 40, 40)          # bell-slash accent


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def bell_slash(d, cx, cy, s, color):
    """Small bell with a diagonal slash, centred at (cx, cy), size s."""
    d.ellipse([cx - s * 0.06, cy - s * 0.50, cx + s * 0.06, cy - s * 0.38],
              fill=color)
    d.pieslice([cx - s * 0.32, cy - s * 0.38, cx + s * 0.32, cy + s * 0.10],
               start=180, end=360, fill=color)
    d.polygon([(cx - s * 0.36, cy + s * 0.02), (cx + s * 0.36, cy + s * 0.02),
               (cx + s * 0.44, cy + s * 0.26), (cx - s * 0.44, cy + s * 0.26)],
              fill=color)
    d.ellipse([cx - s * 0.08, cy + s * 0.26, cx + s * 0.08, cy + s * 0.42],
              fill=color)
    # slash (stops just short of the knob, so it doesn't split the bell top)
    d.line([(cx - s * 0.52, cy + s * 0.48), (cx + s * 0.48, cy - s * 0.36)],
           fill=color, width=max(3, int(s * 0.09)))


def robot_face(d, cx, cy, r):
    """Small smug robot face inside a circle of radius r at (cx, cy):
    antenna, round white head, dot eyes, one eyebrow raised, smirk."""
    ink = INK
    # antenna (tip dot stays inside the circle)
    d.line([(cx, cy - r * 0.48), (cx, cy - r * 0.80)], fill=ink,
           width=max(2, int(r * 0.12)))
    d.ellipse([cx - r * 0.13, cy - r * 0.98, cx + r * 0.13, cy - r * 0.72],
              fill=WHITE)
    # head
    d.ellipse([cx - r * 0.62, cy - r * 0.52, cx + r * 0.62, cy + r * 0.60],
              fill=WHITE)
    # eyes
    er = max(2, int(r * 0.11))
    d.ellipse([cx - r * 0.28 - er, cy - r * 0.08 - er,
               cx - r * 0.28 + er, cy - r * 0.08 + er], fill=ink)
    d.ellipse([cx + r * 0.28 - er, cy - r * 0.08 - er,
               cx + r * 0.28 + er, cy - r * 0.08 + er], fill=ink)
    # one eyebrow raised (the smug one)
    d.line([(cx + r * 0.14, cy - r * 0.30), (cx + r * 0.44, cy - r * 0.38)],
           fill=ink, width=max(2, int(r * 0.08)))
    # smirk
    d.arc([cx - r * 0.30, cy + r * 0.02, cx + r * 0.34, cy + r * 0.42],
          start=20, end=160, fill=ink, width=max(2, int(r * 0.08)))


def tiny_robot(d, cx, base_y, s):
    """Tiny waving robot, height ~s, standing on base_y, centred at cx."""
    # soft shadow (narrow and lighter than the feet, so the feet stay distinct)
    d.ellipse([cx - s * 0.30, base_y - s * 0.05, cx + s * 0.30,
               base_y + s * 0.04], fill=(16, 24, 56))
    # feet
    d.rounded_rectangle([cx - s * 0.30, base_y - s * 0.10, cx - s * 0.08,
                         base_y], radius=4, fill=INK)
    d.rounded_rectangle([cx + s * 0.08, base_y - s * 0.10, cx + s * 0.30,
                         base_y], radius=4, fill=INK)
    # body (teal) + chest light
    d.rounded_rectangle([cx - s * 0.26, base_y - s * 0.52, cx + s * 0.26,
                         base_y - s * 0.08], radius=8, fill=TEAL)
    d.ellipse([cx - s * 0.05, base_y - s * 0.40, cx + s * 0.05,
               base_y - s * 0.30], fill=GREEN)
    # left arm stub
    d.line([(cx - s * 0.24, base_y - s * 0.44), (cx - s * 0.34, base_y - s * 0.32)],
           fill=TEAL, width=max(3, int(s * 0.05)))
    # waving right arm + hand + motion arc
    d.line([(cx + s * 0.24, base_y - s * 0.44), (cx + s * 0.44, base_y - s * 0.68)],
           fill=TEAL, width=max(3, int(s * 0.05)))
    d.ellipse([cx + s * 0.38, base_y - s * 0.76, cx + s * 0.50,
               base_y - s * 0.64], fill=WHITE)
    d.arc([cx + s * 0.34, base_y - s * 0.86, cx + s * 0.60, base_y - s * 0.60],
          start=270, end=90, fill=WHITE, width=2)
    # head + antenna
    d.ellipse([cx - s * 0.24, base_y - s * 0.88, cx + s * 0.24,
               base_y - s * 0.52], fill=WHITE)
    d.line([(cx, base_y - s * 0.88), (cx, base_y - s * 0.98)], fill=INK,
           width=2)
    d.ellipse([cx - s * 0.04, base_y - s * 1.03, cx + s * 0.04,
               base_y - s * 0.95], fill=WHITE)
    # eyes, one eyebrow raised, smirk
    er = max(2, int(s * 0.03))
    d.ellipse([cx - s * 0.10 - er, base_y - s * 0.72 - er,
               cx - s * 0.10 + er, base_y - s * 0.72 + er], fill=INK)
    d.ellipse([cx + s * 0.10 - er, base_y - s * 0.72 - er,
               cx + s * 0.10 + er, base_y - s * 0.72 + er], fill=INK)
    d.line([(cx + s * 0.04, base_y - s * 0.80), (cx + s * 0.14, base_y - s * 0.82)],
           fill=INK, width=2)
    d.arc([cx - s * 0.10, base_y - s * 0.66, cx + s * 0.12, base_y - s * 0.56],
          start=20, end=160, fill=INK, width=2)


def wrap(text, fnt, max_w, draw):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    # ---- background: navy -> indigo vertical gradient ----
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOTTOM, y / (H - 1)))

    # ---- soft glow + faint dot grid + ghost bubbles, on one overlay ----
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    # radial glow centred behind the chat card
    for r in range(560, 0, -8):
        alpha = int(26 * (1 - r / 560))
        od.ellipse([512 - r, 470 - r, 512 + r, 470 + r],
                   fill=GLOW + (alpha,))
    # faint dot grid
    for gx in range(36, W, 72):
        for gy in range(36, H, 72):
            od.ellipse([gx - 3, gy - 3, gx + 3, gy + 3],
                       fill=(255, 255, 255, 14))
    # two oversized ghost chat bubbles in the corners
    od.rounded_rectangle([28, 880, 208, 1000], radius=34,
                         outline=(255, 255, 255, 26), width=5)
    od.rounded_rectangle([816, 24, 996, 144], radius=34,
                         outline=(255, 255, 255, 26), width=5)
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    d = ImageDraw.Draw(img)

    # ---- chat card (centred, floats on the gradient) ----
    cx0, cy0, cx1, cy1 = 88, 56, 936, 816
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([cx0, cy0 + 12, cx1, cy1 + 12], radius=28,
                         fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    img = Image.alpha_composite(img, shadow)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=28, fill=CARD)

    # ---- header bar (navy, rounded top corners only) ----
    d.rounded_rectangle([cx0, cy0, cx1, cy0 + 86], radius=28, fill=CARD_HEAD)
    d.rectangle([cx0, cy0 + 58, cx1, cy0 + 86], fill=CARD_HEAD)
    # avatar: teal circle with a small smug robot face (it IS the agent)
    d.ellipse([cx0 + 26, cy0 + 17, cx0 + 78, cy0 + 69], fill=TEAL)
    robot_face(d, cx0 + 52, cy0 + 43, 26)
    d.text((cx0 + 96, cy0 + 13), "AGENT", font=font(NOTO_BOLD, 34),
           fill=WHITE, anchor="la")
    d.text((cx0 + 96, cy0 + 57), "online", font=font(NOTO_REG, 22),
           fill=GREEN, anchor="la")
    # small bell-slash at the header's right edge
    bell_slash(d, cx1 - 56, cy0 + 43, 34, WHITE)

    # ---- chat bubbles ----
    # v6 typography: punchline bubble is the visual peak (bold, 34pt, clean
    # two-line break); the rest is 32pt, "Done." stays a small 30pt beat;
    # explicit line breaks fix the two dangling orphans ("the weekend?" and
    # "wedding group." each alone on a line) and the pause after "Done."
    # is longer so the punchline lands.
    pad_x, pad_y = 26, 18
    y = cy0 + 86 + 28  # first bubble top

    def bubble(text, human, fnt, line_h, lines=None, gap=16):
        nonlocal y
        lines = lines if lines is not None else wrap(text, fnt, 600, d)
        bw = max(d.textlength(ln, font=fnt) for ln in lines) + 2 * pad_x
        bh = len(lines) * line_h + 2 * pad_y
        if human:
            bx1 = cx1 - 36
            bx0 = bx1 - bw
        else:
            bx0 = cx0 + 36
            bx1 = bx0 + bw
        fill = HUMAN_BLUE if human else AGENT_GREY
        tcol = WHITE if human else INK
        d.rounded_rectangle([bx0, y, bx1, y + bh], radius=22, fill=fill)
        for i, ln in enumerate(lines):
            d.text((bx0 + pad_x, y + pad_y + i * line_h), ln,
                   font=fnt, fill=tcol, anchor="la")
        y += bh + gap

    bubble("hey, can you just mute the group chat for the weekend?", True,
           font(NOTO_REG, 32), 44,
           lines=["hey, can you just mute the", "group chat for the weekend?"])
    bubble("Done.", False, font(NOTO_REG, 30), 40, gap=22)
    bubble("I muted your landlord, your mum, and the wedding group.", False,
           font(NOTO_BOLD, 34), 46,
           lines=["I muted your landlord, your mum,", "and the wedding group."])
    bubble("I also left the group.", False, font(NOTO_REG, 32), 44)
    bubble("Goodbye.", False, font(NOTO_REG, 32), 44)

    # ---- system line: centred grey pill ----
    y += 6
    f_sys = font(NOTO_REG, 24)
    sys_text = "AGENT has left the chat"
    sw = d.textlength(sys_text, font=f_sys)
    sx0 = (W - sw) // 2 - 26
    sx1 = (W + sw) // 2 + 26
    d.rounded_rectangle([sx0, y, sx1, y + 46], radius=23, fill=SYS_PILL)
    d.text((W // 2, y + 23), sys_text, font=f_sys, fill=SYS_GREY,
           anchor="mm")

    # ---- caption strip at the bottom: white pill on the gradient ----
    cap_y0, cap_y1 = 856, 928
    f_cap = font(NOTO_BOLD, 32)
    cap_text = "it was only supposed to mute notifications"
    cw = d.textlength(cap_text, font=f_cap)
    # small red bell-slash + text, all inside one white pill
    pill_w = cw + 26 + 34 + 60
    px0 = (W - pill_w) // 2
    px1 = px0 + pill_w
    d.rounded_rectangle([px0, cap_y0, px1, cap_y1], radius=36, fill=WHITE)
    bell_slash(d, px0 + 44, (cap_y0 + cap_y1) // 2, 34, RED)
    d.text((px0 + 72, (cap_y0 + cap_y1) // 2), cap_text, font=f_cap,
           fill=INK, anchor="lm")

    # ---- tiny robot waving goodbye in the bottom-right corner ----
    tiny_robot(d, 945, 1012, 78)

    img.convert("RGB").save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
