"""
MetaCog-Bench cover — B&W minimalist.
Pure black. Oversized type. One idea. No filler.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = "/Users/admin/Kaggle/metacog-bench/cover.png"


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    # Pure black canvas
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # Top-left: tiny serial-number style mark
    label_font = load_font(22, bold=True)
    d.text((60, 50), "METACOGNITION / 01", font=label_font, fill=(255, 255, 255))

    # Top-right: index mark
    idx_font = load_font(22, bold=True)
    idx_text = "BENCHMARK — AGI"
    idx_bbox = d.textbbox((0, 0), idx_text, font=idx_font)
    idx_w = idx_bbox[2] - idx_bbox[0]
    d.text((W - idx_w - 60, 50), idx_text, font=idx_font, fill=(255, 255, 255))

    # Thin rule under the top row
    d.line([(60, 92), (W - 60, 92)], fill=(255, 255, 255), width=1)

    # Massive centered title — stacked on two lines
    title_font = load_font(170, bold=True)
    line1 = "METACOG"
    line2 = "BENCH."
    b1 = d.textbbox((0, 0), line1, font=title_font)
    b2 = d.textbbox((0, 0), line2, font=title_font)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    x1 = (W - w1) // 2
    y1 = 200
    x2 = (W - w2) // 2
    y2 = y1 + h1 + 10
    d.text((x1, y1), line1, font=title_font, fill=(255, 255, 255))
    d.text((x2, y2), line2, font=title_font, fill=(255, 255, 255))

    # Tagline under
    tag_font = load_font(32, bold=False)
    tagline = "does it know what it knows?"
    tb = d.textbbox((0, 0), tagline, font=tag_font)
    tw = tb[2] - tb[0]
    d.text(((W - tw) // 2, y2 + h2 + 50),
           tagline, font=tag_font, fill=(200, 200, 200))

    # Bottom rule + attribution
    d.line([(60, H - 92), (W - 60, H - 92)], fill=(255, 255, 255), width=1)

    bot_font = load_font(20, bold=True)
    d.text((60, H - 65), "CALIBRATION · ANSWERABILITY · ERROR DETECTION",
           font=bot_font, fill=(255, 255, 255))

    attr_font = load_font(20, bold=False)
    attr_text = "KAGGLE × DEEPMIND"
    ab = d.textbbox((0, 0), attr_text, font=attr_font)
    aw = ab[2] - ab[0]
    d.text((W - aw - 60, H - 65), attr_text, font=attr_font,
           fill=(255, 255, 255))

    img.save(OUT, "PNG", optimize=True)
    print(f"Saved: {OUT}  ({W}x{H})")


if __name__ == "__main__":
    main()
