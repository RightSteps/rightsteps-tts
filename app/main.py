from fastapi import FastAPI, Request
from .api.tts import router
from .response import http_response

app = FastAPI(
    title='RightStep Voice',
    version='1.0.0',
    docs_url=None,
    redoc_url=None,
)

app.include_router(router)


@app.get('/health')
async def health(request: Request):
    return http_response(request, 200, 'Health check passed successfully')
