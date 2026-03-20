from sqlalchemy import Column, Integer, String

from backend.app.models.base import BaseModel


class AdminUser(BaseModel):
    """Single admin account used by the management console."""

    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
