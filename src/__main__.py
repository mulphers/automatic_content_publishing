from fast_depends import dependency_provider

from src.common.markers.gateway import TransactionGatewayMarker
from src.core.settings import load_settings
from src.database import TransactionGateway
from src.database.core.connection import create_engine


def main() -> None:
    settings = load_settings()

    database_engine = create_engine(
        host=settings.database.host,
        port=settings.database.port
    )

    dependency_provider.override(
        original=TransactionGatewayMarker,
        override=TransactionGateway(engine=database_engine)
    )


if __name__ == '__main__':
    main()
