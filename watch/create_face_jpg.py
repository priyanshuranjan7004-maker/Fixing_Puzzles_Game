
import math
from PIL import Image, ImageDraw, ImageFont

width = 320
height = 240
face = min(width, height)
ofs = (width - face) // 2

out = Image.new("RGB", (width, height), (255, 255, 255))

fnt = ImageFont.truetype("./LibreBaskerville-Regular.ttf", 18)
d = ImageDraw.Draw(out)
radius = int(face // 2  * 0.8)
cx = int(face // 2)

second = 0
for minute in range(1, 60):
    angle = ((minute*math.pi/30)+(second*math.pi/1800))
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    y1 = -cx * cos_a * 0.76
    x1 = cx * sin_a * 0.76

    y2 = -cx * cos_a * 0.7
    x2 = cx * sin_a * 0.7

    d.line([ofs+x1+cx, y1+cx, ofs+x2+cx, y2+cx], width=1, fill="#000000")

for hour in range(1, 13):
    angle = (hour*math.pi/6)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    y1 = -cx * cos_a * 0.76
    x1 = cx * sin_a * 0.76

    y2 = -cx * cos_a * 0.7
    x2 = cx * sin_a * 0.7

    d.line([ofs+x1+cx, y1+cx, ofs+x2+cx, y2+cx], width=5, fill="#ff0000")

    y = -cx * cos_a * 0.9
    x = cx * sin_a * 0.9

    size = d.textbbox((0, 0), str(hour), font=fnt)
    d.text(
        (ofs+x+cx-((size[2]+size[0] >> 1)), y+cx-((size[3]+size[1]) >> 1)),
        str(hour),
        font=fnt,
        fill=(0, 0, 0),
        align="center")

out.save(f'face_{width}x{height}.jpg', "JPEG")
