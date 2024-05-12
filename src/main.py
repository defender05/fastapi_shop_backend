# Logging
from loguru import logger as log

# FastAPI
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager

# Database
from redis import asyncio as aioredis

# Routes
from src.users.router import auth_router, user_router
from src.catalog.router import catalog_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    log.info("🚀 Starting application")
    # Подключаемся к redis для кэширование результатов запросов
    redis = aioredis.from_url("redis://localhost/0", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    log.info("⛔ Stopping application")


app = FastAPI(title="FastAPI Shop", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:6000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(catalog_router)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


# Маршрут для отображения главной страницы
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://localhost:5000/docs">Swagger Docs</a><br>
    <a href="http://localhost:5000/redoc">ReDoc</a>
    """

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, port=5000, host="127.0.0.1")
