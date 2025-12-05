import logging

from fastapi import APIRouter
from fastapi import Query
from fastapi import Path
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from starlette.responses import JSONResponse, StreamingResponse

from app.models import dto
from app.services import user
from app.core import dependencies
from app.utils.api_response import ApiResponse
from app.utils.api_exception import ApiException


router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# Sử dụng tokenUrl tương đối so với app `api` (mount ở /api)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.get("/me", response_model=dto.ApiResponse)
def get_me(user: dependencies.user_dependency, token: str = Depends(oauth2_scheme)) -> JSONResponse:
    try:
        return ApiResponse.success(data=user.model_dump(), message="Lấy thông tin tài khoản thành công")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.get("/all", response_model=dto.ApiResponse)
def get_all(limit: int = Query(1000, gt=0), offset: int = Query(0, ge=0)):
    try:
        logging.info(f"Get all {limit}/{offset}")
        users = user_service.get_all(limit, offset)
        payload = [user.model_dump() for user in users]
        return ApiResponse.success(data=payload, message="Danh sách người dùng")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.get("/admin_only", response_model=dto.ApiResponse)
def get_admin_only(user: dependencies.admin_dependency):
    try:
        return ApiResponse.success(data=user.model_dump(), message="Thông tin admin")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.get("/{id}", response_model=dto.ApiResponse)
def get_by_id(id: int = Path(ge=1)):
    try:
        user = user_service.get_by_id_dto(id)
        return ApiResponse.success(data=user.model_dump(), message="Lấy người dùng thành công")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)

@router.get("/email/{email}", response_model=dto.ApiResponse)
def get_by_email(email: str):
    try:
        user = user_service.get_by_email_dto(email)
        return ApiResponse.success(data=user.model_dump(), message="Lấy người dùng thành công")
    except ApiException as e:
        return ApiResponse.error(message=e.message, status=e.status_code)