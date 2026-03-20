from sqlalchemy import Column, Integer, String, Text

from backend.app.models.base import BaseModel, SortableActiveMixin


class Product(BaseModel, SortableActiveMixin):
    """Product content block used by the brand and product showcase section."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    subtitle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)
    specs_json = Column(Text, nullable=True)
