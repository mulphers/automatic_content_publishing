import logging
from threading import Thread
from time import sleep
from typing import Annotated, Never

from fast_depends import Depends, inject

from src.common.dto.content import ContentDTO
from src.common.interfaces.abstract_content_finder import AbstractContentFinder
from src.common.interfaces.abstract_content_unique_checker import \
    AbstractContentUniqueChecker
from src.common.markers.gateway import TransactionGatewayMarker
from src.core.logger import init_logger
from src.core.settings import Settings
from src.database import DatabaseGateway


class App:
    def __init__(
            self,
            settings: Settings,
            content_finder: AbstractContentFinder,
            content_unique_checker: AbstractContentUniqueChecker
    ) -> None:
        self.settings = settings
        self.content_finder = content_finder
        self.content_unique_checker = content_unique_checker

    @inject
    def _drop_pending_content(
            self,
            gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
            content: list[ContentDTO]
    ) -> None:
        count_pending_content = self.content_unique_checker.drop_pending_content(
            gateway=gateway,
            content=content
        )

        logging.debug(f'Drop pending content: {count_pending_content}')

    @inject
    def _find_new_content(
            self, gateway: Annotated[DatabaseGateway, Depends(TransactionGatewayMarker)],
            content: list[ContentDTO]
    ) -> list[ContentDTO]:
        return self.content_unique_checker.find_new_content(
            gateway=gateway,
            content=content
        )

    def _start_polling(self, url: str, headers: dict, cookies: dict) -> Never:
        self._drop_pending_content(  # type: ignore[call-arg]
            content=self.content_finder.find_content(
                url=url,
                headers=headers,
                cookies=cookies
            )
        )

        while True:
            found_content = self.content_finder.find_content(  # type: ignore[call-arg]
                url=url,
                headers=headers,
                cookies=cookies
            )

            new_content = self._find_new_content(  # type: ignore[call-arg]
                content=found_content
            )

            logging.debug(f'All content found: {len(found_content)}')
            logging.debug(f'New content found: {new_content}')

            sleep(30)

    def _start_thread(self) -> None:
        for thread_id, account_parsing_settings in enumerate(self.settings.account_parsing):
            Thread(
                target=self._start_polling,
                name=f'thread_{thread_id}',
                args=(account_parsing_settings.url, account_parsing_settings.headers, account_parsing_settings.cookies)
            ).start()

    def start_app(self) -> None:
        init_logger()
        self._start_thread()
