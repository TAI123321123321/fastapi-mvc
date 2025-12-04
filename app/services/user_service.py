from random import randint

from starlette import status

from app.models import db
from app.models import dto
from app.models import enums
from app.repository import user_repo

from app.core.security import bcrypt_hashing
from app.utils import formatting
from app.exceptions.scheme import AppException

MIN_PASS = 100000
MAX_PASS = 999999


def get_all(limit: int = 1000, offset: int = 0) -> list[dto.UserDTO]:
    return [user.to_dto() for user in user_repo.get(limit, offset)]


def get_by_id(id: int) -> db.UserDb:
    user = user_repo.get_by_id(id)
    if user is None:
        raise AppException(message="User not found", status_code=status.HTTP_400_BAD_REQUEST)

    return user


def get_by_id_dto(id: int) -> dto.UserDTO:
    user = get_by_id(id)
    return user.to_dto()


def get_by_email(email: str) -> db.UserDb:
    email_form = formatting.format_string(email)
    user = user_repo.get_by_email(email_form)
    if user is None:
        raise AppException(message="User not found", status_code=status.HTTP_400_BAD_REQUEST)

    return user


def get_by_email_dto(email: str) -> dto.UserDTO:
    user = get_by_email(email)
    return user.to_dto()


def create_user(obj: dto.UserCreateDTO) -> dto.UserDTO:
    user = _create(obj, enums.UserRole.USER)
    return user.to_dto()


def create_admin(obj: dto.UserCreateDTO) -> dto.UserDTO:
    user = _create(obj, enums.UserRole.ADMIN)
    return user.to_dto()


def update_name(user: db.UserDb, obj: dto.UserUpdateNameDTO) -> None:
    user.name = formatting.format_string(obj.name)
    user.surname = formatting.format_string(obj.surname)
    user_repo.update(user)


def update_password(user: dto.UserDTO, obj: dto.UserUpdatePassDTO) -> None:
    user_db = get_by_id(user.id)
    if bcrypt_hashing.validate(obj.old_password, user_db.password) is False:
        raise AppException(message="Incorrect password", status_code=status.HTTP_400_BAD_REQUEST)

    _update_password(user_db, obj.new_password)


def reset_password(email: str) -> None:
    user = get_by_email(email)
    new_pass = _reset_password(user)
    print(f"New password for {user.email} is '{new_pass}'")


def delete(id: int) -> None:
    user_repo.delete(id)


def _create(obj: dto.UserCreateDTO, role: enums.UserRole) -> db.UserDb:
    name_formatted = formatting.format_string(obj.name)
    surname_formatted = formatting.format_string(obj.surname)
    email_formatted = formatting.format_string(obj.email)
    # password_formatted = formatting.format_string(obj.password)

    if name_formatted == "":
        raise AppException(message="Name is not valid", status_code=status.HTTP_400_BAD_REQUEST)

    if surname_formatted == "":
        raise AppException(message="Surname is not valid", status_code=status.HTTP_400_BAD_REQUEST)

    if email_formatted == "":
        raise AppException(message="Email is not valid", status_code=status.HTTP_400_BAD_REQUEST)

    if user_repo.get_by_email(email_formatted) is not None:
        raise AppException(message="Email already exists", status_code=status.HTTP_400_BAD_REQUEST)

    user_to_db = db.UserDb()
    user_to_db.name = name_formatted
    user_to_db.surname = surname_formatted
    user_to_db.role = role
    user_to_db.email = email_formatted
    # user_to_db.password = password_formatted
    user_to_db.password = bcrypt_hashing.hash(obj.password)

    return user_repo.add(user_to_db)


def _update_password(user: db.UserDb, new_password: str) -> None:
    new_pass_hash = bcrypt_hashing.hash(new_password)
    user.password = new_pass_hash
    user_repo.update(user)


def _reset_password(user: db.UserDb) -> str:
    new_password = str(randint(MIN_PASS, MAX_PASS))
    _update_password(user, new_password)

    return new_password
