from functools import wraps
import json
from starlette import status
from app.utils.api_response import ApiResponse
from app.utils.api_exception import ApiException

def params_is_not_null(*required_keys):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Tìm đối tượng request trong args hoặc kwargs
            request = None
            for arg in args:
                if hasattr(arg, 'json') and callable(arg.json):
                    request = arg
                    break
            if not request:
                request = kwargs.get('request') if kwargs.get('request') else kwargs.get('params')
            data = json.loads(request.json())
            for key in required_keys:
                if key not in data or data[key] is None:
                    return ApiResponse.error(message=f"Tham số '{key}' bị thiếu", status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return wrapper
    return decorator