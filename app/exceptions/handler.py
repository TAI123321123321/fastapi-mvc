from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.scheme import AppException
from app.models.dto import ApiResponse
from app.views import common_view


def add_json(app: FastAPI):
    @app.exception_handler(AppException)
    async def exception_handler(request: Request, exc: AppException):
        """
        Handle exceptions and return a JSON response.
        :param request: FastAPI request object
        :param exc: Exception object
        :return: JSON response with error details
        """
        payload = ApiResponse(code=exc.status_code, message=exc.message, data=None)
        return JSONResponse(payload.model_dump(), status_code=exc.status_code)
def add_html(app: FastAPI):
    @app.exception_handler(AppException)
    async def exception_handler(request: Request, exc: AppException):
        return common_view.error_page(request, exc)