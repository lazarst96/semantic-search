from sqlalchemy import Column, String, ARRAY, Float

from src.db.base_class import Base
from src.core.config import settings


class Question(Base):
    text = Column(String(255), nullable=False)
    owner_name = Column(String(32), nullable=True, unique=False, index=True)
    embedding = Column(ARRAY(item_type=Float, dimensions=settings.VECTOR_DIM))
