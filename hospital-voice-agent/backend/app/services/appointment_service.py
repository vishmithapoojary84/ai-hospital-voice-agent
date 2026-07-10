from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database.appointment import Appointment
from app.database.enums import AppointmentStatus
from app.services.patient_service import get_patient_by_phone


def get_patient_appointments(
    db: Session,
    phone: str,
    status: AppointmentStatus | None = None,
):
    patient = get_patient_by_phone(
        db,
        phone,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    query = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == patient.id,
        )
    )

    if status is not None:
        query = query.filter(
            Appointment.status == status,
        )

    appointments = (
        query.order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc(),
        )
        .all()
    )

    return appointments