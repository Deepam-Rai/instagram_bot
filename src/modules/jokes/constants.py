import os
from pathlib import Path


MODULE_PATH = Path(os.path.realpath(__file__)).parent

DEFAULT_BG_IMAGE = 'white_bg.jpg'
DEFAULT_GSHEET_TITLE = "jokes"
DEFAULT_WORKSHEET_TITLE = "jokes"

# columns in gsheet
COL_ID = "id"           # unique id to each joke
COL_JOKE = "joke"       # jokes
COL_POSTED = "posted"   # indicates postes or not
COL_DATE = "date"       # date on which joke is posted
# column values
POSTED_TRUE = "yes"  # value that is set at COL_POSTED for posted jokes
