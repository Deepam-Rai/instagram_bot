"""
Module that is capable of publishing a new insta-post with jokes every day.
"""
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
        self.gclient = self.get_gclient(creds_file_path=gsheet_creds)
        self.gsheet_title = gsheet_title
        self.worksheet_title = worksheet_title

    def get_new_joke(self):
        """
        Returns new joke and background image-path for it.
        :return:
        """
        joke_sheet = self.get_joke_sheet()
        unposted = [x for x in joke_sheet.get_all_records() if x[COL_POSTED] != POSTED_TRUE]
        new_joke = random.choice(unposted)
        bg = MODULE_PATH / 'images' / DEFAULT_BG_IMAGE
        return new_joke, bg

    def get_gclient(self, creds_file_path) -> Client:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_file_path | self.gsheet_creds, scope)
        client = gspread.authorize(creds)
        return client

    def connect_gsheet(self, title: str = None, key: str = None, url: str = None) -> Spreadsheet:
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
        gsheet = self.connect_gsheet(title=self.gsheet_title)
        joke_sheet = gsheet.worksheet(self.worksheet_title)
        return joke_sheet

    def update_gsheet_new_post(self, joke_id: str) -> None:
        joke_sheet = self.get_joke_sheet()
        cols = joke_sheet.get_all_values(major_dimension=Dimension('COLUMNS'))
        cols_name2index = {col[0]: index + 1 for index, col in enumerate(cols)}
        joke_ids = cols[cols_name2index[COL_ID] - 1]
        row_id = joke_ids.index(str(joke_id)) + 1
        updates = {COL_POSTED: POSTED_TRUE, COL_DATE: date.today()}
        for col_name, value in updates.items():
            joke_sheet.update_cell(row_id, cols_name2index[col_name], str(value))

    def publish_new_joke(self, logo_last: bool = True) -> bool:
        joke_dict, image_path = self.get_new_joke()
        joke = joke_dict[COL_JOKE]
        joke_id = joke_dict[COL_ID]
        image_writer = ImageWriter()
        post_image = image_writer.draw_quote(joke, image_path)
        post_image.show()
        if query_yes_no("Post image?") is True:
            save_path = MODULE_PATH / f'posted/{date.today()}_{joke_id}.jpg'
            post_image.save(save_path)
            if logo_last:
                self.publisher.publish_album(paths=[save_path, MODULE_PATH / 'images/logo.jpg'])
            else:
                self.publisher.publish_photo(save_path)
            self.update_gsheet_new_post(joke_id)
            logger.info(f"New post: {joke}")
            return True
        else:
            logger.warning(f"Nothing posted")
            return False
