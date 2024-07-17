from pathlib import Path
from instagrapi import Client
import logging


logger = logging.getLogger(__name__)


class InstaPublisher:
    def __init__(self, insta_creds: dict):
        self.client = Client()
        logger.info("Logging into instagram...")
        self.client.login(insta_creds["username"], insta_creds["password"])

    def publish_photo(self, path: Path, caption: str = None):
        self.client.photo_upload(path, caption)

    def publish_album(self, paths: list[Path], caption: str = None):
        self.client.album_upload(paths, caption)
