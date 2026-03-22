from sqlalchemy import Boolean, Column, Integer, String

from backend.app.models.base import BaseModel


class SiteSetting(BaseModel):
    """Generic site-level settings used for homepage and footer presentation."""

    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(120), nullable=True)
    description = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)