from time import sleep

import requests

from src.common.dto.content import ContentDTO
from src.common.interfaces.abstract_content_downloader import \
    AbstractContentDownloader
from src.common.types import PathToContent


class ContentDownloaderFromTikTok(AbstractContentDownloader):
    def download_content(self, content: list[ContentDTO]) -> list[PathToContent]:
        paths_to_content: list[PathToContent] = []

        for item in content:
            sleep(25)

            response = requests.get(url=item.url)

            with open(file=f'src/storage/content/{item.content_id}.mp4', mode='wb') as file:
                file.write(response.content)
                paths_to_content.append(f'src/storage/content/{item.content_id}.mp4')

        return paths_to_content
