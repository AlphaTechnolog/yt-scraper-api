import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YoutubeScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=self.options)

    def _open_channel(self, channel_id: str):
        self.driver.get(f"https://youtube.com/{channel_id}/videos")

    def _open_video(self, video_id: str):
        self.driver.get(f"https://youtube.com/watch?v={video_id}")

    def _wait_for_element(self, query: tuple):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(query)
        )

    def _wait_for_elements(self, query: tuple):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(query)
        )

    def close_driver(self):
        self.driver.close()

    def get_channel_videos(self, channel_id: str):
        self._open_channel(channel_id)

        try:
            links_elements = self.driver.find_elements(By.XPATH, '//a[@id="video-title-link" and @href != "" and not(contains(@href, "shorts"))]')
            links = [link.get_attribute('href') for link in links_elements]
        finally:
            self.close_driver()

        return links or []

    def search(self, query: str, skip_shorts: bool = False):
        self.driver.get(f"https://youtube.com/results?search_query={query}")

        try:
            shorts_skips = ' and not(contains(@href, "shorts"))' if skip_shorts else ''
            links_elements = self._wait_for_elements((By.XPATH, f'//div[@id="title-wrapper" and contains(@class, "ytd-video-renderer")]/h3[@class="title-and-badge style-scope ytd-video-renderer"]/a[@id="video-title" and @href and @title and @aria-label{shorts_skips}]'))
            links = [link.get_attribute('href') for link in links_elements]
        finally:
            self.close_driver()

        return links or []

    def get_video_details(self, video_hash: str) -> dict:
        self._open_video(video_hash)

        try:
            title_element = self._wait_for_element((By.XPATH, '//h1[contains(@class, "ytd-watch-metadata")]/yt-formatted-string'))
            author_link = self._wait_for_element((By.XPATH, '//yt-formatted-string[contains(@class, "ytd-channel-name")]/a[@href]'))
            avatar = self._wait_for_element((By.XPATH, '//ytd-video-owner-renderer/a[@href]/yt-img-shadow[@id="avatar" and contains(@class, "ytd-video-owner-renderer")]/img[@id="img" and contains(@class, "yt-img-shadow") and @src]'))
            subs_label = self._wait_for_element((By.XPATH, '//div[@id="upload-info" and contains(@class, "ytd-video-owner-renderer")]/yt-formatted-string[@id="owner-sub-count" and contains(@class, "ytd-video-owner-renderer")]'))
            likes = self._wait_for_element((By.XPATH, '//ytd-toggle-button-renderer[@class="style-scope ytd-segmented-like-dislike-button-renderer"]//div[contains(@class, "yt-spec-button-shape-next--button-text-content")]/span[@role="text" and @class="yt-core-attributed-string yt-core-attributed-string--white-space-no-wrap"]'))

            recommended_videos = [{
                'url': i.get_attribute('href'),
                'hash': re.sub(r'^.*v=([a-zA-Z0-9_-]+).*$', r'\1', i.get_attribute('href'))
            } for i in self._wait_for_elements(
                (By.XPATH, '//div[contains(@class, "metadata") and contains(@class, "ytd-compact-video-renderer")]/a[@class="yt-simple-endpoint style-scope ytd-compact-video-renderer" and @href and @href != ""]')
            )]

            details = {
                'title': title_element.text,
                'likes': likes.text,
                'recommended_videos': recommended_videos,
                'author_info': {
                    'name': author_link.text,
                    'id': author_link.get_attribute('href').split('/')[-1],
                    'href': author_link.get_attribute('href'),
                    'subs': subs_label.text,
                    'avatar': {
                        'src': avatar.get_attribute('src'),
                    }
                },
            }
        finally:
            self.close_driver()

        return details or {
            'error': 'Cannot get details!'
        }
