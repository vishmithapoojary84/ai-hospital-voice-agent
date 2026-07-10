from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Time,
    ForeignKey,
    Enum,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
from app.database.enums import DayOfWeek


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False
    )

    day_of_week = Column(
        Enum(DayOfWeek),
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )

    doctor = relationship(
        "Doctor",
        back_populates="schedules"
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "day_of_week",
            "start_time",
        "end_time",
        name="uq_doctor_schedule",
    ),
)