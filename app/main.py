from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import http_error_handler
from app.api.users import router as user_router

app = FastAPI(title=settings.app_name)

# Error handling
app.add_exception_handler(Exception, http_error_handler)

# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Include user-related routes
app.include_router(user_router, prefix="/api", tags=["users"])