from fastapi import FastAPI
from app.core.config import settings
from app.core.exceptions import http_error_handler
from app.api.users import router as user_router
from app.api.coach import router as coach_router
from app.api.coachee import router as coachee_router

app = FastAPI(title=settings.app_name)

# Error handling
app.add_exception_handler(Exception, http_error_handler)

# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Include user-related routes
app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(coach_router, prefix="/api", tags=["coach"])
app.include_router(coachee_router, prefix="/api", tags=["coachee"])