from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class ApiResponse:
    @staticmethod
    def success(data=None, message="Thành công", status=200, **kwargs):
        response = {
            "code": status,
            "status": "success",
            "message": message,
            "data": jsonable_encoder(data),
        }
        response.update(kwargs)
        return JSONResponse(content=response, status_code=status)

    @staticmethod
    def error(message="Thất bại", status=400, errors=None):
        response = {
            "code": status,
            "status": "error",
            "message": message,
        }
        if errors:
            response["errors"] = jsonable_encoder(errors)
        return JSONResponse(content=response, status_code=status)