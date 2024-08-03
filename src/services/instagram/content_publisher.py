import logging
from time import sleep

from selenium.webdriver.common.by import By

from src.common.interfaces.abstract_content_publisher import \
    AbstractContentPublisher
from src.common.types import PathToContent
from src.common.webdriver.chrome import ChromeWebdriver
from src.core.settings import Settings
from src.utils.selectors.instagram import *  # noqa


class InstagramContentPublisher(AbstractContentPublisher):
    def __init__(self, settings: Settings, webdriver: ChromeWebdriver) -> None:
        self.settings = settings
        self.webdriver = webdriver

    def _login(self) -> None:
        if not self.webdriver.load_cookies(
                url='https://www.instagram.com/',
                account_username=self.settings.instagram.username
        ):
            self._enter_account_data()

        self.webdriver.driver.refresh()

    def _enter_account_data(self) -> None:
        self.webdriver.send_keys(
            by=By.CSS_SELECTOR,
            value=INPUT_USERNAME,
            data=self.settings.instagram.username
        )

        self.webdriver.send_keys(
            by=By.CSS_SELECTOR,
            value=INOUT_PASSWORD,
            data=self.settings.instagram.password
        )

        self.webdriver.click_button(
            by=By.CSS_SELECTOR,
            value=LOG_IN_BUTTON
        )

        sleep(5)

        self.webdriver.save_cookies(account_username=self.settings.instagram.username)

    def _close_window(self, window_by: By, window_value: str, button_by: By, button_value: str) -> None:
        if self.webdriver.check_exist_element(by=window_by, value=window_value):
            self.webdriver.click_button(by=button_by, value=button_value)

    def _set_content_size_9_to_16(self) -> None:
        self.webdriver.click_button(by=By.CSS_SELECTOR, value=EDIT_SIZE_BUTTON)
        self.webdriver.click_button(by=By.CSS_SELECTOR, value=SIZE_9_BY_16_BUTTON)

    def _publish_content(self, path: PathToContent) -> None:
        self.webdriver.click_button(
            by=By.CSS_SELECTOR,
            value=NEW_PUBLISHED_BUTTON
        )

        self.webdriver.send_keys(
            by=By.CSS_SELECTOR,
            value=INPUT_CONTENT_TO_FORM,
            data=f'{self.settings.root_dir()}/{path}'
        )

        self._close_window(
            window_by=By.CSS_SELECTOR, window_value=REELS_NOTIFICATION_WINDOW,
            button_by=By.CSS_SELECTOR, button_value=CLOSE_REELS_NOTIFICATION_BUTTON
        )

        self._set_content_size_9_to_16()

        self.webdriver.click_button(by=By.CSS_SELECTOR, value=NEXT_BUTTON)
        self.webdriver.click_button(by=By.CSS_SELECTOR, value=NEXT_BUTTON)

        self.webdriver.click_button(
            by=By.CSS_SELECTOR,
            value=INPUT_HASHTAGS
        )

        self.webdriver.send_keys(
            by=By.CSS_SELECTOR,
            value=INPUT_HASHTAGS,
            data=self.settings.hashtags.to_str()
        )

        self.webdriver.click_button(by=By.CSS_SELECTOR, value=NEXT_BUTTON)

        sleep(10)

        logging.debug(f'Content {path} published')

        self.webdriver.driver.refresh()

    def publish_content(self, paths: list[PathToContent]) -> None:
        with self.webdriver.driver:
            self.webdriver.create_new_tab()
            self._login()

            self._close_window(
                window_by=By.CSS_SELECTOR,
                window_value=NOTIFICATION_WINDOW,
                button_by=By.CSS_SELECTOR,
                button_value=CLOSE_NOTIFICATION_BUTTON
            )

            for path in paths:
                self._publish_content(path=path)
