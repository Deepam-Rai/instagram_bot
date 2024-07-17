import os
from pathlib import Path


MODULE_PATH = Path(os.path.realpath(__file__)).parent

DEFAULT_BG_IMAGE = 'white_bg.jpg'
DEFAULT_GSHEET_TITLE = "jokes"
DEFAULT_WORKSHEET_TITLE = "jokes"
DEFAULT_CAPTION = (
    f"Just sharing funny finds!! ^-^\n"
    f"\n"
    f"#jokes #jokedigest"
)


# columns in gsheet
COL_ID = "id"           # unique id to each joke
COL_JOKE = "joke"       # jokes
COL_POSTED = "posted"   # indicates posted or not
COL_DATE = "date"       # date on which joke is posted
COL_CAPTION = "caption"
# column values
POSTED_TRUE = "yes"  # value that is set at COL_POSTED for posted jokes
