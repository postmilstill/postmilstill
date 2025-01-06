# routers/__init__.py
from fastapi import APIRouter
from .quotes import router as quotes_router

# Create a master router to include all sub-routers
router = APIRouter()

# Include the quotes router
router.include_router(quotes_router)