from fastapi import Request
from fastapi.responses import JSONResponse


def http_response(request: Request, status_code: int, message: str, data=None):
    return JSONResponse(
        status_code=status_code,
        content={
            'success': True,
            'statusCode': status_code,
            'request': {
                'method': request.method,
                'url': str(request.url.path),
            },
            'message': message,
            'data': data,
        },
    )


def http_error(request: Request, status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            'success': False,
            'statusCode': status_code,
            'request': {
                'method': request.method,
                'url': str(request.url.path),
            },
            'message': message,
            'data': None,
        },
    )
