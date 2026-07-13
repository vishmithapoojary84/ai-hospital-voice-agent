from __future__ import annotations
from sqlalchemy import Time, ForeignKey, Enum as SAEnum, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import time, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.doctor import Doctor
from app.database.database import Base
from app.database.enums import DayOfWeek

class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(SAEnum(DayOfWeek), nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    doctor: Mapped["Doctor"] = relationship(
        "Doctor",
        back_populates="schedules"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
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
