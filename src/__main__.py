from fast_depends import dependency_provider

from src.common.markers.gateway import TransactionGatewayMarker
from src.core.app import App
from src.core.settings import load_settings
from src.database import TransactionGateway
from src.database.core.connection import create_engine
from src.services.tik_tok.content_downloader import ContentDownloaderFromTikTok
from src.services.tik_tok.content_finder import TikTokContentFinder
from src.services.tik_tok.content_unique_checker import \
    ContentUniqueCheckerWithDatabase
from src.services.instagram.content_publisher import InstagramContentPublisher
from src.common.webdriver.chrome import ChromeWebdriver


def main() -> None:
    settings = load_settings()

    app = App(
        settings=settings,
        content_finder=TikTokContentFinder(),
        content_unique_checker=ContentUniqueCheckerWithDatabase(),
        content_downloader=ContentDownloaderFromTikTok(),
        content_publisher=InstagramContentPublisher(
            settings=settings,
            webdriver=ChromeWebdriver()
        )
    )

    database_engine = create_engine(
        host=settings.database.host,
        port=settings.database.port
    )

    dependency_provider.override(
        original=TransactionGatewayMarker,
        override=TransactionGateway(engine=database_engine)
    )

    app.start_app()


if __name__ == '__main__':
    main()
