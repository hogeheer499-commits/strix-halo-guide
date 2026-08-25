#!/usr/bin/env python3
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
DOCS_ASSETS = ROOT / "docs" / "assets"

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
    ("101.0", "t/s", "Direct Qwen3-Coder"),
    ("140.4", "t/s", "CHADROCK MTP server"),
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
title = "AMD Strix Halo Local LLM Guide"
title_font = font_bold(36)
bbox = draw.textbbox((0, 0), title, font=title_font)
draw.text(((W - bbox[2] + bbox[0]) // 2, 380), title, fill=WHITE, font=title_font)

# Punchline
punch = "Copyable setup · cross-OEM validation · raw CSV/log evidence"
punch_font = font_reg(26)
bbox = draw.textbbox((0, 0), punch, font=punch_font)
draw.text(((W - bbox[2] + bbox[0]) // 2, 435), punch, fill=ACCENT, font=punch_font)

# GitHub handle bottom
handle = "github.com/hogeheer499-commits/strix-halo-guide"
handle_font = font_reg(18)
bbox = draw.textbbox((0, 0), handle, font=handle_font)
draw.text(((W - bbox[2] + bbox[0]) // 2, H - 50), handle, fill=DIM, font=handle_font)

DOCS_ASSETS.mkdir(parents=True, exist_ok=True)
preview_outputs = [ROOT / "social-preview.png", DOCS_ASSETS / "social-preview.png"]
for output in preview_outputs:
    img.save(output, "PNG", optimize=True)

# A current-model share card for the Qwen3.8 route comparison. The large
# numbers deliberately keep measured-local and external-corrected evidence
# separate instead of presenting community fork peaks as guide-owned results.
qwen = Image.new("RGB", (W, H), BG)
qwen_draw = ImageDraw.Draw(qwen)
qwen_draw.rectangle([0, 0, W, 4], fill=ACCENT)

eyebrow = "CURRENT MODEL DECISION GUIDE"
eyebrow_font = font_bold(20)
qwen_draw.text((70, 54), eyebrow, fill=ACCENT, font=eyebrow_font)

qwen_title = "Qwen3.8 27B on AMD Strix Halo"
qwen_title_font = font_black(48)
qwen_draw.text((70, 92), qwen_title, fill=WHITE, font=qwen_title_font)

qwen_subtitle = "Official easy path · direct/MTP controls · context-correctness evidence"
qwen_subtitle_font = font_bold(23)
qwen_draw.text((72, 162), qwen_subtitle, fill=DIM, font=qwen_subtitle_font)

qwen_stats = [
    ("20.4", "t/s", "measured official Ollama"),
    ("50K", "", "exact local retrieval"),
    ("262K", "class", "external corrected route"),
]
qwen_section_w = (W - 140) // 3
qwen_num_font = font_black(67)
qwen_unit_font = font_bold(28)
qwen_label_font = font_bold(19)
for i, (num, unit, label) in enumerate(qwen_stats):
    cx = 70 + qwen_section_w * i + qwen_section_w // 2
    num_bbox = qwen_draw.textbbox((0, 0), num, font=qwen_num_font)
    num_w = num_bbox[2] - num_bbox[0]
    unit_w = 0
    if unit:
        unit_bbox = qwen_draw.textbbox((0, 0), unit, font=qwen_unit_font)
        unit_w = unit_bbox[2] - unit_bbox[0] + 12
    start_x = cx - (num_w + unit_w) // 2
    qwen_draw.text((start_x, 235), num, fill=WHITE, font=qwen_num_font)
    if unit:
        qwen_draw.text((start_x + num_w + 12, 276), unit, fill=ACCENT, font=qwen_unit_font)
    label_bbox = qwen_draw.textbbox((0, 0), label, font=qwen_label_font)
    label_w = label_bbox[2] - label_bbox[0]
    qwen_draw.text((cx - label_w // 2, 327), label, fill=DIM, font=qwen_label_font)

qwen_draw.rectangle([70, 390, W - 70, 391], fill="#21262d")
comparison = "Why 20, 31, 52 and 65 t/s are not the same claim"
comparison_font = font_bold(28)
comparison_bbox = qwen_draw.textbbox((0, 0), comparison, font=comparison_font)
qwen_draw.text(
    ((W - (comparison_bbox[2] - comparison_bbox[0])) // 2, 430),
    comparison,
    fill=WHITE,
    font=comparison_font,
)
qwen_footer = "Model · quant · backend · fork · speculation · prompt · context · evidence"
qwen_footer_font = font_bold(19)
qwen_footer_bbox = qwen_draw.textbbox((0, 0), qwen_footer, font=qwen_footer_font)
qwen_draw.text(
    ((W - (qwen_footer_bbox[2] - qwen_footer_bbox[0])) // 2, 486),
    qwen_footer,
    fill=ACCENT,
    font=qwen_footer_font,
)
qwen_handle = "github.com/hogeheer499-commits/strix-halo-guide"
qwen_handle_bbox = qwen_draw.textbbox((0, 0), qwen_handle, font=handle_font)
qwen_draw.text(
    ((W - (qwen_handle_bbox[2] - qwen_handle_bbox[0])) // 2, H - 50),
    qwen_handle,
    fill=DIM,
    font=handle_font,
)

qwen_preview_outputs = [
    ROOT / "qwen38-route-preview.png",
    DOCS_ASSETS / "qwen38-route-preview.png",
]
for output in qwen_preview_outputs:
    qwen.save(output, "PNG", optimize=True)

# A stable, square icon for browser tabs and eligible search-result favicons.
icon_size = 512
icon = Image.new("RGB", (icon_size, icon_size), BG)
icon_draw = ImageDraw.Draw(icon)
icon_draw.rectangle([0, 0, icon_size, 12], fill=ACCENT)

icon_font = font_black(210)
icon_text = "SH"
icon_bbox = icon_draw.textbbox((0, 0), icon_text, font=icon_font)
icon_x = (icon_size - (icon_bbox[2] - icon_bbox[0])) // 2
icon_y = 92
icon_draw.text((icon_x, icon_y), icon_text, fill=WHITE, font=icon_font)

llm_font = font_bold(54)
llm_text = "LOCAL AI"
llm_bbox = icon_draw.textbbox((0, 0), llm_text, font=llm_font)
llm_x = (icon_size - (llm_bbox[2] - llm_bbox[0])) // 2
icon_draw.text((llm_x, 355), llm_text, fill=ACCENT, font=llm_font)
icon.save(DOCS_ASSETS / "favicon.png", "PNG", optimize=True)

print("Done: social-preview.png, qwen38-route-preview.png, and docs/assets SEO images")
