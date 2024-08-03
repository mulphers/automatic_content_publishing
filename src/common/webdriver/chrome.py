import os
import pickle
from time import sleep
from typing import Any

from fake_useragent import UserAgent
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from undetected_chromedriver.options import ChromeOptions


class ChromeWebdriver:
    def __init__(self) -> None:
        self.driver = Chrome(options=self._get_options())
        self._set_driver_settings()

    @staticmethod
    def _get_options() -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument(f'User-Agent:{UserAgent().chrome}')

        return options

    def _set_driver_settings(self) -> None:
        self.driver.implicitly_wait(10)

    @staticmethod
    def _check_exist_cookies(account_username: str) -> bool:
        return os.path.exists(f'src/storage/cookies/{account_username}_cookies.pkl')

    def load_cookies(self, url: str, account_username: str) -> bool:
        self.driver.get(url)

        if self._check_exist_cookies(account_username=account_username):
            self.driver.delete_all_cookies()

            with open(file=f'src/storage/cookies/{account_username}_cookies.pkl', mode='rb') as file:
                cookies = pickle.load(file)

            for cookie in cookies:
                self.driver.add_cookie(cookie)

            return True

        return False

    def save_cookies(self, account_username: str) -> None:
        with open(
                file=f'src/storage/cookies/{account_username}_cookies.pkl',
                mode='wb'
        ) as file:
            pickle.dump(self.driver.get_cookies(), file)

    def check_exist_element(self, by: By, value: str) -> bool:
        try:
            return bool(self.driver.find_element(by=by, value=value))
        except NoSuchElementException:
            return False

    def send_keys(self, by: By, value: str, data: Any) -> None:
        if self.check_exist_element(by=by, value=value):
            keys = self.driver.find_element(by=by, value=value)
            keys.send_keys(data)
            sleep(5)

    def click_button(self, by: By, value: str) -> None:
        if self.check_exist_element(by=by, value=value):
            button = self.driver.find_element(by=by, value=value)
            button.click()
            sleep(5)

    def create_new_tab(self) -> None:
        self.driver.switch_to.new_window()
