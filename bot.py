from credentials import INSTA_CREDS
# from PIL import Image
from instagrapi import Client
from image_writer import ImageWriter
from constants import *


def get_new_text():
    text = """
    text1
    text2 .asdas asdasd
    @text
    #text #texts
    """
    return text


text = get_new_text()
image_path = 'images/white_bg.png'

image_writer = ImageWriter(text, image_path)
image_writer.draw_quote()
image_writer.save_image()
image_writer.show_image()

# cl = Client()
# cl.login(INSTA_CREDS["username"], INSTA_CREDS["password"])
# cl.photo_upload(image_path, caption)
