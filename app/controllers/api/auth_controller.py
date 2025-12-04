from fastapi import APIRouter
from fastapi import status
from fastapi import Response, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models import dto
from app.services import user_service
from app.core.security import session
from app.core import dependencies

from app.utils import validate
from app.utils.api_response import ApiResponse
from app.utils.api_exception import ApiException



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dto.ApiResponse)
async def register(user: dto.UserCreateDTO):
    try:
        created_user = user_service.create_user(user)
        return ApiResponse.success(
            data=created_user.model_dump(),
            message="Đăng ký thành công",
            status=status.HTTP_201_CREATED,
        )
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.post("/login", status_code=status.HTTP_200_OK, response_model=dto.ApiResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), res: Response = None):
    """
    OAuth2 password flow login.
    Swagger/OAuth2PasswordBearer sẽ gửi username/password dạng form-data.
    """
    try:
        credentials = dto.UserLoginDTO(
            email=form_data.username,
            password=form_data.password,
        )
        token = await session.login(credentials, res)
        return ApiResponse.success(
            data={"access_token": token, "token_type": "bearer"},
            message="Đăng nhập thành công",
        )
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.get("/logout", status_code=status.HTTP_200_OK, response_model=dto.ApiResponse)
async def logout(res: Response):
    try:
        await session.logout(res)
        return ApiResponse.success(message="Đăng xuất thành công")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.get("/validate", response_model=dto.ApiResponse)
async def check_session(token: dependencies.token_dependency):
    try:
        return ApiResponse.success(data=token.model_dump(), message="Token hợp lệ")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.put("/password/update", status_code=status.HTTP_200_OK, response_model=dto.ApiResponse)
def update_password(dto: dto.UserUpdatePassDTO, user: dependencies.user_dependency):
    try:
        user_service.update_password(user, dto)
        return ApiResponse.success(message="Đổi mật khẩu thành công")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.post("/password/reset", status_code=status.HTTP_200_OK, response_model=dto.ApiResponse)
def reset_password(email: str):
    try:
        user_service.reset_password(email)
        return ApiResponse.success(message="Đặt lại mật khẩu thành công")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)