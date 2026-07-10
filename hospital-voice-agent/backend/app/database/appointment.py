from sqlalchemy import (
    Column,
    Integer,
    Date,
    Time,
    DateTime,
    ForeignKey,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.database.enums import AppointmentStatus


class Appointment(Base):
    __tablename__ = "appointments"

    

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey(
            "patients.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    doctor_id = Column(
    Integer,
        ForeignKey(
            "doctors.id",
            ondelete="RESTRICT"
        ),
        nullable=False,
    )

    appointment_date = Column(
        Date,
        nullable=False,
    )

    appointment_time = Column(
        Time,
        nullable=False,
    )

    status = Column(
        Enum(AppointmentStatus),
        nullable=False,
        default=AppointmentStatus.BOOKED,
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

    patient = relationship(
        "Patient",
        back_populates="appointments",
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments",
    )

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "appointment_date",
            "appointment_time",
            name="uq_doctor_appointment_slot",
        ),
    )