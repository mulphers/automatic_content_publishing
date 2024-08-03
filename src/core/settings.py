import json
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AccountParsingSettings(BaseSettings):
    url: str
    headers: dict
    cookies: Optional[dict] = None


class InstagramSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_prefix='instagram_',
        extra='ignore'
    )

    username: str
    password: str


class HashtagsSettings(BaseSettings):
    hashtags_list: list[str]

    def to_str(self) -> str:
        return ' '.join(self.hashtags_list)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_prefix='database_',
        extra='ignore'
    )

    uri: str
    host: str
    port: int

    @property
    def url(self) -> str:
        return self.uri.format(self.host, self.port)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='./.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    account_parsing: list[AccountParsingSettings]
    instagram: InstagramSettings
    hashtags: HashtagsSettings
    database: DatabaseSettings
    delay: int

    @staticmethod
    def root_dir() -> Path:
        return Path(__file__).resolve().parent.parent.parent


def _load_account_parsing_settings() -> list[AccountParsingSettings]:
    with open(file='src/storage/headers/account_parsing_headers.json', encoding='utf-8') as file:
        data = json.load(fp=file)

    return [AccountParsingSettings(url=settings['url'], headers=settings['headers']) for settings in data]


def _load_hashtags_settings() -> HashtagsSettings:
    with open(file='src/storage/hashtags/hashtags.json', encoding='utf-8') as file:
        return HashtagsSettings(hashtags_list=json.load(file))


def load_settings(
        account_parsing: Optional[list[AccountParsingSettings]] = None,
        instagram: Optional[InstagramSettings] = None,
        hashtags: Optional[HashtagsSettings] = None,
        database: Optional[DatabaseSettings] = None
) -> Settings:
    return Settings(
        account_parsing=account_parsing or _load_account_parsing_settings(),
        instagram=instagram or InstagramSettings(),  # type: ignore[call-arg]
        hashtags=hashtags or _load_hashtags_settings(),
        database=database or DatabaseSettings()  # type: ignore[call-arg]
    )
