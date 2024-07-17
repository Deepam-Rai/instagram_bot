from credentials.insta_credentials import INSTA_CREDS
from credentials.jokes_digest_service_account_key import GSERVICE_ACC_KEY
from src.modules.jokes.jokes import Jokes
import logging
import coloredlogs
from constants import *


logging.basicConfig()
logger = logging.getLogger(__name__)
coloredlogs.install(
    level=logging.INFO,
    logger=logger,
    fmt='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s():%(lineno)s: %(message)s',
    field_styles=LOGGER_FIELD_STYLE,
    level_styles=LOGGER_LEVEL_STYLES
)


joke_module = Jokes(
    insta_creds=INSTA_CREDS,
    gsheet_creds=GSERVICE_ACC_KEY,
    gsheet_title="jokes",
    worksheet_title="jokes"
)
joke_module.publish_new_joke()
