from backend.app import models  # noqa: F401
from backend.app.core.database import Base, SessionLocal, engine
from backend.app.services.init_data import seed_admin, seed_content
from backend.app.services.schema_sync import ensure_legacy_columns


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    ensure_legacy_columns(engine)

    session = SessionLocal()
    try:
        seed_admin(session)
        seed_content(session)
    finally:
        session.close()
    print("Database initialized and demo data seeded.")
