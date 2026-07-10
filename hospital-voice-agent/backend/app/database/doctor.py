from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.database.enums import Specialty


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    specialty = Column(
        Enum(Specialty),
        nullable=False,
        index=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    schedules = relationship(
        "DoctorSchedule",
        back_populates="doctor",
        cascade="all, delete-orphan",
    )

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
    )