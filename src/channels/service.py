import re
from src.channels.scraper import YoutubeScraper


class YoutubeService:
    def _open_scraper(self):
        if not hasattr(self, 'scraper') or self.scraper is None:
            self.scraper = YoutubeScraper()

    def _close_scraper(self):
        if hasattr(self, 'scraper'):
            self.scraper = None

    def get_channel_videos(self, channel_id: str):
        self._open_scraper()
        try:
            videos = self.scraper.get_channel_videos(channel_id)
        finally:
            self._close_scraper()

        return videos or []

    def get_video_hash(self, video_url: str):
        return re.sub(r'^.*v=([a-zA-Z0-9_-]+).*$', r'\1', video_url)

    def search(self, query: str, skip_shorts: bool = False):
        self._open_scraper()
        try:
            videos = self.scraper.search(query, skip_shorts)
        finally:
            self._close_scraper()

        return videos or []

    def get_video_details(self, video_hash: str) -> dict:
        self._open_scraper()
        try:
            details = self.scraper.get_video_details(video_hash)
        finally:
            self._close_scraper()

        return details or []
