from sqlalchemy import Column, Integer, String

from backend.app.models.base import BaseModel, SortableActiveMixin


class FooterQRCode(BaseModel, SortableActiveMixin):
    """Footer QR code items rendered as a configurable multi-item list."""

    __tablename__ = "footer_qr_codes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=True)
    description = Column(String(255), nullable=True)
    image_url = Column(String(500), nullable=True)
