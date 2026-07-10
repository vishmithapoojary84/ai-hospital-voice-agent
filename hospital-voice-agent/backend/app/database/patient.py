from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database.database import Base
from sqlalchemy.orm import relationship

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(String(15), unique=True, nullable=False)

    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )