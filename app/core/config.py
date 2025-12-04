from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from os import getenv
import os


def _get_from_env(var_name: str) -> str:
    value = getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' must be set.")
    return value

@dataclass(frozen=True)
class Config:
    DB_CONNECTION_STRING: str
    COOKIES_KEY_NAME: str
    SESSION_TIME: timedelta
    HASH_SALT: str

    @staticmethod
    def get_config() -> Config:
        user = "taivip123"
        password = "1"
        host = "localhost:5432"
        database_name = "demo_fast"
        # uri_db = os.getenv("URI_DB", "")
        default_conn = f"postgresql+psycopg2://{user}:{password}@{host}/{database_name}"
        db_connection_string = getenv("DB_CONNECTION_STRING", default_conn)
        if db_connection_string == "":
            raise ValueError(
                "Environment variable 'DB_CONNECTION_STRING' must be set and cannot be empty. "
            )

        cookies_key_name = "session_token"
        session_time = timedelta(days=30)
        hash_salt = getenv("HASH_SALT", "SomeRandomStringHere")

        return Config(db_connection_string, cookies_key_name, session_time, hash_salt)


CONFIG = Config.get_config()
