from fastapi import APIRouter, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.views import main_view
from app.core.dependencies import user_dependency
from app.core.security import session
from app.models import dto
from app.services import user as user_service
from app.exceptions.scheme import AppException
import logging
# Get logger for this module
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="",
    tags=["Pages"],
    default_response_class=HTMLResponse
)

@router.get("/")
def main(req: Request):
    return main_view.main_page(req)

@router.get("/register")
def register_get(req: Request):
    """Display registration form"""
    return main_view.register_page(req)

@router.post("/register")
async def register_post(
    req: Request,
    name: str = Form(...),
    surname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle registration form submission"""
    logger.info(f"Yêu cầu đăng ký từ email: {email}")
    try:
        user_data = dto.UserCreateDTO(
            name=name,
            surname=surname,
            email=email,
            password=password
        )
        created_user = user_service.create_user(user_data)
        logger.info(f"Đăng ký thành công cho email: {email}")
        return main_view.register_page(req, success="Đăng ký thành công! Bạn có thể đăng nhập ngay.")
    except AppException as e:
        logger.warning(f"Đăng ký thất bại cho email: {email} - Lỗi: {e.message}")
        return main_view.register_page(req, error=e.message)
    except Exception as e:
        logger.error(f"Lỗi không mong đợi khi đăng ký: {str(e)}")
        return main_view.register_page(req, error="Đã xảy ra lỗi. Vui lòng thử lại sau.")

@router.post("/login")
async def login_post(
    req: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    """Handle login form submission and redirect to cf.goplay.vn on success"""
    logger.info(f"Yêu cầu đăng nhập từ email: {email}")
    try:
        credentials = dto.UserLoginDTO(email=email, password=password)
        # Use 303 See Other for POST redirect (more appropriate than 302)
        res = RedirectResponse(url="https://cf.goplay.vn/", status_code=303)
        token = await session.login(credentials, res)
        logger.info(f"Đăng nhập thành công cho email: {email} - Redirecting to https://cf.goplay.vn/")
        return res
    except AppException as e:
        logger.warning(f"Đăng nhập thất bại cho email: {email} - Lỗi: {e.message}")
        # On error, redirect back to main page with error message
        # You can customize this to show error message on the login page
        return RedirectResponse(url="/", status_code=302)

@router.get("/check")
def check(req: Request, user: user_dependency):
    return main_view.auth_page(req, user)
