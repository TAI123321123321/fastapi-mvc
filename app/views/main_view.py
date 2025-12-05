from datetime import datetime

from fastapi.requests import Request
from app.models.dto import UserDTO
from app.core.templates import templates


def main_page(req: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        req, "main.jinja", {"date": now.replace(microsecond=0)}
    )

def register_page(req: Request, error: str = None, success: str = None):
    now = datetime.now()
    return templates.TemplateResponse(
        req, "register.jinja", {
            "date": now.replace(microsecond=0),
            "error": error,
            "success": success
        }
    )

def auth_page(req: Request, user: UserDTO):
    return templates.TemplateResponse(
        req, "auth.jinja", {"user": user}
    )