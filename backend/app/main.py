from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import get_settings
from backend.app.core.database import Base, SessionLocal, engine
from backend.app.routers import auth, banners, news, products, public, sections, site_settings
from backend.app.services.init_data import seed_admin, seed_content
from backend.app.services.schema_sync import ensure_legacy_columns

# Import all models before metadata creation so SQLAlchemy can discover tables.
from backend.app import models  # noqa: F401


settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = Path(__file__).resolve().parents[1] / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")


@app.get("/")
def health_check():
    """Basic health endpoint for quick deployment verification."""
    return {"message": f"{settings.app_name} API is running"}


@app.on_event("startup")
def on_startup() -> None:
    """Create tables and seed first-run data so the local project is usable immediately."""
    Base.metadata.create_all(bind=engine)
    ensure_legacy_columns(engine)
    session = SessionLocal()
    try:
        seed_admin(session)
        seed_content(session)
    finally:
        session.close()


app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(public.router, prefix=settings.api_v1_prefix)
app.include_router(banners.router, prefix=settings.api_v1_prefix)
app.include_router(sections.router, prefix=settings.api_v1_prefix)
app.include_router(products.router, prefix=settings.api_v1_prefix)
app.include_router(news.router, prefix=settings.api_v1_prefix)
app.include_router(site_settings.router, prefix=settings.api_v1_prefix)