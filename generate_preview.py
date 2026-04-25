#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 640
BG = "#0d1117"
WHITE = "#ffffff"
ACCENT = "#58a6ff"  # GitHub blue accent
DIM = "#8b949e"     # GitHub muted text

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

font_black = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Black.ttf", s)
font_bold = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", s)
font_reg = lambda s: ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf", s)

# Subtle top border accent line
draw.rectangle([0, 0, W, 4], fill=ACCENT)

# Three big numbers side by side
stats = [
    ("87", "t/s", "MoE inference"),
    ("70B+", "", "parameter models"),
    ("128", "GB", "unified memory"),
]

num_font = font_black(82)
unit_font = font_bold(40)
label_font = font_reg(22)

section_w = W // 3
y_numbers = 160

for i, (num, unit, label) in enumerate(stats):
    cx = section_w * i + section_w // 2

    full_text = num + " " + unit if unit else num
    bbox = draw.textbbox((0, 0), full_text, font=num_font)
    tw = bbox[2] - bbox[0]

    if unit:
        num_bbox = draw.textbbox((0, 0), num + " ", font=num_font)
        num_w = num_bbox[2] - num_bbox[0]
        start_x = cx - tw // 2

        draw.text((start_x, y_numbers), num + " ", fill=WHITE, font=num_font)

        unit_bbox = draw.textbbox((0, 0), unit, font=unit_font)
        unit_y = y_numbers + (bbox[3] - bbox[1]) - (unit_bbox[3] - unit_bbox[1]) - 4
        draw.text((start_x + num_w, unit_y), unit, fill=ACCENT, font=unit_font)
    else:
        start_x = cx - tw // 2
        draw.text((start_x, y_numbers), full_text, fill=WHITE, font=num_font)

    label_bbox = draw.textbbox((0, 0), label, font=label_font)
    label_w = label_bbox[2] - label_bbox[0]
    draw.text((cx - label_w // 2, y_numbers + 95), label, fill=DIM, font=label_font)

# Divider line
y_div = 340
draw.rectangle([140, y_div, W - 140, y_div + 1], fill="#21262d")

# Title
title = "The definitive Strix Halo LLM guide"
title_font = font_bold(36)
bbox = draw.textbbox((0, 0), title, font=title_font)
draw.text(((W - bbox[2] + bbox[0]) // 2, 380), title, fill=WHITE, font=title_font)

# Punchline
punch = "Beats DGX Spark for $1,400 less"
punch_font = font_reg(26)
bbox = draw.textbbox((0, 0), punch, font=punch_font)
draw.text(((W - bbox[2] + bbox[0]) // 2, 435), punch, fill=ACCENT, font=punch_font)

# GitHub handle bottom
handle = "github.com/hogeheer499-commits/strix-halo-guide"
handle_font = font_reg(18)
bbox = draw.textbbox((0, 0), handle, font=handle_font)
draw.text(((W - bbox[2] + bbox[0]) // 2, H - 50), handle, fill=DIM, font=handle_font)

img.save("/home/hoge-heer/strix-halo-guide/social-preview.png", "PNG")
print("Done: social-preview.png (1280x640)")
