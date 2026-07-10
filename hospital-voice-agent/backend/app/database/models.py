from sqlalchemy import Column, Integer, String, Boolean

from app.database.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    specialty = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)