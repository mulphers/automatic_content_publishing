from typing import Optional

import requests

from src.common.dto.content import ContentDTO
from src.common.interfaces.abstract_content_finder import AbstractContentFinder


class TikTokContentFinder(AbstractContentFinder):
    def find_content(self, url: str, headers: dict, cookies: Optional[dict] = None) -> list[ContentDTO]:
        response = requests.get(
            url=url,
            headers=headers,
            cookies=cookies or {}
        ).json()

        return [
            ContentDTO(
                content_id=item['id'],
                url=item['video']['bitrateInfo'][0]['PlayAddr']['UrlList'][-1],
                description=item['desc']
            ) for item in response['itemList']
        ]
