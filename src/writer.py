from PIL import Image, ImageDraw, ImageFont
import textwrap
from src.constants import *


class ImageWriter:

    def __init__(
            self,
            font=DEFAULT_FONT,
            font_size=FONT_SIZE
    ) -> None:
        self.font_color = FONT_COLOR
        self.font = font
        self.font_size = font_size

    def draw_quote(
            self,
            text,
            img_path,
            text_color=None,
            text_font=None,
            font_size=None
    ) -> Image.Image:
        text_font = text_font or self.font
        font_size = font_size or self.font_size
        use_font = ImageFont.truetype(f'src/fonts/{text_font}', font_size)
        text_color = text_color or self.font_color
        img = Image.open(img_path)
        img = self.adjust_image(img)
        MAX_W, MAX_H = img.size
        vertical_pos = MAX_H * VERT_OFFSET
        draw = ImageDraw.Draw(img)

        current_h, pad = vertical_pos, PARA_PADDING
        for joke_para in text.split("\n"):
            para = textwrap.wrap(joke_para, width=PARA_WIDTH)
            if len(para) > 0:
                for line in para:
                    _, _, w, h = draw.textbbox((0, 0), text=line, font=use_font)
                    draw.text((((MAX_W - w) / 2), current_h),
                              line, font=use_font, fill=text_color)
                    current_h += h + pad
                current_h += h + (pad * 2)
        return img

    def adjust_image(self, image):
        if image.mode != "RGB":
            image = image.convert("RGB")
        return image
