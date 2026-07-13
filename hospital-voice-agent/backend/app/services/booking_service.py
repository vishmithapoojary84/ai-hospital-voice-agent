

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.appointment import Appointment
from app.services.patient_service import get_or_create_patient
from app.services.doctor_service import get_doctor_by_id
from app.services.availability_service import get_available_slots
from app.database.enums import AppointmentStatus
from datetime import date, time
from app.services.validation_service import (
    validate_appointment_datetime,
)


def create_appointment(
    db: Session,
    patient_id: int,
    doctor_id: int,
    appointment_date: date,
    appointment_time: time,
):
    existing_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appointment_date,
            Appointment.appointment_time == appointment_time,
        )
        .first()
    )

    if existing_appointment:
        if existing_appointment.status == AppointmentStatus.CANCELLED:
            existing_appointment.patient_id = patient_id
            existing_appointment.status = AppointmentStatus.SCHEDULED
            try:
                db.commit()
                db.refresh(existing_appointment)
                return existing_appointment
            except Exception:
                db.rollback()
                raise
        else:
            raise HTTPException(
                status_code=400,
                detail="Slot already booked.",
            )

    appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
    )
    

    try:
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
        return appointment

    except Exception:
        db.rollback()
        raise


def book_appointment(
    db: Session,
    patient_name: str,
    phone: str,
    doctor_id: int,
    appointment_date: date,
    appointment_time: time,
):

    validate_appointment_datetime(
        appointment_date,
        appointment_time,
    )
    
    patient = get_or_create_patient(
    db,
    patient_name,
    phone,
    )

    doctor = get_doctor_by_id(
    db,
    doctor_id,
    )

    if doctor is None:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found.",
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Doctor is not available.",
        )

    available_slots = get_available_slots(
    db,
    doctor_id,
    appointment_date,
    )

    if appointment_time not in available_slots:
        raise HTTPException(
            status_code=409,
            detail="Requested time slot is not available.",
        )
    return create_appointment(
        db,
        patient.id,
        doctor_id,
        appointment_date,
        appointment_time,
    )


def get_appointment_by_id(
    db: Session,
    appointment_id: int,
):
    return (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
        )
        .first()
    )


def cancel_appointment(
    db: Session,
    appointment_id: int,
):
    appointment = get_appointment_by_id(
        db,
        appointment_id,
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found.",
        )

    if appointment.status == AppointmentStatus.CANCELLED:
        raise HTTPException(
            status_code=409,
            detail="Appointment is already cancelled.",
        )

    appointment.status = AppointmentStatus.CANCELLED

    try:
        db.commit()
        db.refresh(appointment)

    except Exception:
        db.rollback()
        raise

    return {
        "message": "Appointment cancelled successfully."
    }



def reschedule_appointment(
    db: Session,
    appointment_id: int,
    appointment_date: date,
    appointment_time: time,
):
    validate_appointment_datetime(
        appointment_date,
        appointment_time,
    )

    appointment = get_appointment_by_id(
        db,
        appointment_id,
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found.",
        )

    if appointment.status in [
        AppointmentStatus.CANCELLED,
        AppointmentStatus.COMPLETED,
    ]:
        raise HTTPException(
            status_code=409,
            detail="This appointment cannot be rescheduled.",
        )
    
    available_slots = get_available_slots(
        db,
        appointment.doctor_id,
        appointment_date,
    )

    if appointment_time not in available_slots:
        raise HTTPException(
            status_code=409,
            detail="Requested time slot is not available.",
        )

    appointment.appointment_date = appointment_date
    appointment.appointment_time = appointment_time
    
    try:
        db.commit()
        db.refresh(appointment)

    except Exception:
        db.rollback()
        raise

    return appointment