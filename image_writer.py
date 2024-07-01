from PIL import Image, ImageDraw, ImageFont
import textwrap
from constants import *


class ImageWriter:

    def __init__(
            self,
            text,
            img_path,
            font=DEFAULT_FONT,
            font_size=FONT_SIZE,
            font_color=FONT_COLOR
    ) -> None:
        self.my_font = ImageFont.truetype(f'fonts/{font}', font_size)
        self.img = Image.open(img_path)
        self.adjust_image()
        self.MAX_W, self.MAX_H = self.img.size
        self.text_color = font_color
        self.text = text

    def draw_quote(self) -> None:
        vertical_pos = self.MAX_H * VERT_OFFSET
        draw = ImageDraw.Draw(self.img)

        current_h, pad = vertical_pos, PARA_PADDING
        for joke_para in self.text.split("\n"):
            para = textwrap.wrap(joke_para, width=PARA_WIDTH)
            if len(para) > 0:
                for line in para:
                    _, _, w, h = draw.textbbox((0, 0), text=line, font=self.my_font)
                    draw.text((((self.MAX_W - w) / 2), current_h),
                              line, font=self.my_font, fill=self.text_color)
                    current_h += h + pad
                current_h += h + (pad * 2)

    def show_image(self) -> None:
        self.img.show()

    def save_image(self) -> None:
        self.img.save('tmpImage.jpg')

    def adjust_image(self) -> None:
        if self.img.mode != "RGB":
            self.img = self.img.convert("RGB")
