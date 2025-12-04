from time import time
from random import randint

import hashlib
import bcrypt

from app.core.config import CONFIG


def _prepare_bytes(secret: str) -> bytes:
    """
    Build a consistent byte sequence to feed bcrypt.
    SHA-256 digest -> always 32 bytes, well under the 72 byte limit.
    """
    material = f"{secret}{CONFIG.HASH_SALT}".encode("utf-8")
    return hashlib.sha256(material).digest()


def hash(password: str) -> str:
    prepared = _prepare_bytes(password)
    hashed = bcrypt.hashpw(prepared, bcrypt.gensalt())
    return hashed.decode("utf-8")


def validate(plain_password: str, hashed_password: str) -> bool:
    try:
        prepared = _prepare_bytes(plain_password)
        return bcrypt.checkpw(prepared, hashed_password.encode("utf-8"))
    except Exception as exc:
        print(exc)
        return False


def random_hash() -> str:
    timestamp = time()
    random_number = randint(0, 999999)
    prepared = _prepare_bytes(f"{timestamp} {random_number}")
    return bcrypt.hashpw(prepared, bcrypt.gensalt()).decode("utf-8")

