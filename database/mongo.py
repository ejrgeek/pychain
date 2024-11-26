from pymongo import MongoClient
from threading import Lock

from dotenv import load_dotenv
import os

from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

class MongoDBSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                user = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
                password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "password")
                host = os.getenv("MONGO_HOST", "localhost")
                port = os.getenv("MONGO_PORT", "27017")
                db_name = os.getenv("DB_NAME", "blockchain_db")
                uri = f"mongodb://{user}:{password}@{host}:{port}/"
                cls._instance._initialize(uri, db_name)
        return cls._instance

    def _initialize(self, uri, db_name):
        self._client = MongoClient(uri)
        self._db = self._client[db_name]

    def get_collection(self, collection_name):
        return self._db[collection_name]

    def close(self):
        self._client.close()
