import logging
from typing import Optional
from datetime import date
import requests

from src.writer import ImageWriter
from .constants import DEFAULT_BG_IMAGE, MODULE_PATH
from .utils import query_yes_no

logger = logging.getLogger(__name__)


class Quotes:
    def __init__(self):
        pass

    def fetch_new_quote(self) -> Optional[str]:
        """
        Fetches new quote.
        Returns:
            New quote as `str` if found, else None.
        """
        try:
            response = requests.get(
                url="https://zenquotes.io/api/quotes/",
            )
            response.raise_for_status()
            return response.json()[0]["q"]
        except Exception as e:
            logger.error(f'Error fetching new quote: {e}')
            return None

    def get_image_path(self, quote: str):
        """
        Given a quote, returns path to the fitting background image.
        Returns:
        """
        return MODULE_PATH / 'images' / DEFAULT_BG_IMAGE


    def get_new(self):
        """
        Gets new post.
        Returns:
        """
        new_quote = self.fetch_new_quote()
        if new_quote is None:
            logger.error(f'Could not fetch new quote.')
            return None
        image_path = self.get_image_path(new_quote)
        image_writer = ImageWriter()
        post_image = image_writer.draw_quote(new_quote, image_path)
        post_image.show()
        if query_yes_no("Post image?") is True:
            save_path = MODULE_PATH / f'posted/{date.today()}.jpg'
            post_image.save(save_path)
            caption = "#motivation"
            # self.publisher.publish_photo(path=save_path, caption=caption)
            logger.info(f"New post:\nquote:\n{new_quote}\ncaption:\n{caption}")
            return True
        else:
            logger.warning(f"Nothing posted.")
            return False
