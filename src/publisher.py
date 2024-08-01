from pathlib import Path
from instagrapi import Client
import logging


logger = logging.getLogger(__name__)


class InstaPublisher:
    def __init__(self, insta_creds: dict):
        self.creds = insta_creds
        self.client: Client = None

    def login(self) -> None:
        logger.info("Logging into instagram...")
        self.client = Client()
        self.client.login(self.creds["username"], self.creds["password"])

    def publish_photo(self, path: Path, caption: str = None):
        if self.client is None:
            self.login()
        self.client.photo_upload(path=path, caption=caption)

    def publish_album(self, paths: list[Path], caption: str = None):
        if self.client is None:
            self.login()
        self.client.album_upload(paths=paths, caption=caption)
