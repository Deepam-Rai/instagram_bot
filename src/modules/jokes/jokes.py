from .constants import *
from src.writer import ImageWriter
from src.publisher import InstaPublisher
import logging
import random
from datetime import date
import gspread
from gspread import Spreadsheet, Client, Worksheet
from gspread.utils import Dimension
from oauth2client.service_account import ServiceAccountCredentials
from .utils import *


FILE_PATH = MODULE_PATH / __name__
logger = logging.getLogger(__name__)


class Jokes:
    def __init__(
            self,
            insta_creds,
            gsheet_creds,
            gsheet_title: str = DEFAULT_GSHEET_TITLE,
            worksheet_title: str = DEFAULT_WORKSHEET_TITLE
    ):
        self.insta_creds = insta_creds
        self.publisher = InstaPublisher(insta_creds=self.insta_creds)
        self.gsheet_creds = gsheet_creds
        self.gclient = self.get_gclient(gsheet_creds=gsheet_creds)
        self.gsheet_title = gsheet_title
        self.worksheet_title = worksheet_title

    def get_new_joke(self) -> (dict, Path):
        """
        Returns new joke and background image-path for it.
        :return: jokes_dict (joke, id, etc) and path to background image.
                If no new joke to post, then returns None, None
        """
        joke_sheet = self.get_joke_sheet()
        unposted = [x for x in joke_sheet.get_all_records() if x[COL_POSTED] != POSTED_TRUE]
        if len(unposted) == 0:
            return None, None
        new_joke = random.choice(unposted)
        bg = MODULE_PATH / 'images' / DEFAULT_BG_IMAGE
        return new_joke, bg

    def get_gclient(self, gsheet_creds) -> Client:
        """
        Returns client to the gsheet.
        :param gsheet_creds:
        :return:
        """
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(gsheet_creds | self.gsheet_creds, scope)
        client = gspread.authorize(creds)
        return client

    def connect_gsheet(self, title: str = None, key: str = None, url: str = None) -> Spreadsheet:
        """
        Returns the google spreadsheet.
        :param title:
        :param key:
        :param url:
        :return:
        """
        if title:
            sheet = self.gclient.open(title)
        elif key:
            sheet = self.gclient.open_by_key(key)
        elif url:
            sheet = self.gclient.open_by_url(url)
        else:
            raise ValueError("You must provide either a title, key, or url to connect to the Google Sheet.")
        return sheet

    def get_joke_sheet(self) -> Worksheet:
        """
        Returns specific sheet that contains joke inside given spreadsheet.
        :return:
        """
        gsheet = self.connect_gsheet(title=self.gsheet_title)
        joke_sheet = gsheet.worksheet(self.worksheet_title)
        return joke_sheet

    def update_gsheet_new_post(self, joke_id: str) -> None:
        """
        Updates gsheet column values to indicate new joke has been posted.
        :param joke_id:
        :return:
        """
        joke_sheet = self.get_joke_sheet()
        cols = joke_sheet.get_all_values(major_dimension=Dimension('COLUMNS'))
        cols_name2index = {col[0]: index + 1 for index, col in enumerate(cols)}
        joke_ids = cols[cols_name2index[COL_ID] - 1]
        row_id = joke_ids.index(str(joke_id)) + 1
        updates = {COL_POSTED: POSTED_TRUE, COL_DATE: date.today()}
        for col_name, value in updates.items():
            joke_sheet.update_cell(row_id, cols_name2index[col_name], str(value))

    def publish_new_joke(self, logo_last: bool = True) -> bool:
        """
        Fetches new joke. Writes on image. Posts it.
        :param logo_last: If true, then an album is posted with logo image at the last.
        :return: Success or not as True or False
        """
        joke_dict, image_path = self.get_new_joke()
        if joke_dict is None:
            logger.error("No new joke to post!!")
            return False
        joke = joke_dict[COL_JOKE]
        joke_id = joke_dict[COL_ID]
        caption = (joke_dict[COL_CAPTION] + "\n" + DEFAULT_CAPTION).strip()
        image_writer = ImageWriter()
        post_image = image_writer.draw_quote(joke, image_path)
        post_image.show()
        if query_yes_no("Post image?") is True:
            save_path = MODULE_PATH / f'posted/{date.today()}_{joke_id}.jpg'
            post_image.save(save_path)
            if logo_last:
                self.publisher.publish_album(paths=[save_path, MODULE_PATH/'images/logo.jpg'], caption=caption)
            else:
                self.publisher.publish_photo(path=save_path, caption=caption)
            self.update_gsheet_new_post(joke_id)
            logger.info(f"New post:\njoke:\n{joke}\ncaption:\n{caption}")
            return True
        else:
            logger.warning(f"Nothing posted")
            return False
