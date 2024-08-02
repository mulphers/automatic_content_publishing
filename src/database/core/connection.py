from odmantic import SyncEngine
from pymongo import MongoClient


def create_engine(host: str, port: int, direct_connection: bool = True) -> SyncEngine:
    return SyncEngine(
        client=MongoClient(
            host=host,
            port=port,
            directConnection=direct_connection
        )
    )
