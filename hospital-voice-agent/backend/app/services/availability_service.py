from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.database.appointment import Appointment
from app.database.doctor_schedule import DoctorSchedule
from app.services.doctor_service import get_doctors_by_specialty
from app.database.enums import Specialty
from app.database.enums import (
    DayOfWeek,
    AppointmentStatus,
)


def get_doctor_schedule(
    db: Session,
    doctor_id: int,
    day_of_week: DayOfWeek,
):
    return (
        db.query(DoctorSchedule)
        .filter(
            DoctorSchedule.doctor_id == doctor_id,
            DoctorSchedule.day_of_week == day_of_week,
        )
        .first()
    )

def generate_time_slots(
    start_time,
    end_time,
):
    slots = []

    current = datetime.combine(
        date.today(),
        start_time,
    )

    end = datetime.combine(
        date.today(),
        end_time,
    )

    while current < end:
        slots.append(current.time())
        current += timedelta(minutes=30)

    return slots

def get_booked_slots(
    db: Session,
    doctor_id: int,
    appointment_date: date,
):
    appointments = (
    db.query(Appointment)
    .filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status != AppointmentStatus.CANCELLED,
    )
    .all()
    )

    return [
        appointment.appointment_time
        for appointment in appointments
    ]


def get_available_slots(
    db: Session,
    doctor_id: int,
    appointment_date: date,
):
    day_of_week = DayOfWeek(
        appointment_date.strftime("%A")
    )

    schedule = get_doctor_schedule(
        db,
        doctor_id,
        day_of_week,
    )

    if schedule is None:
        return []

    slots = generate_time_slots(
        schedule.start_time,
        schedule.end_time,
    )

    booked_slots = get_booked_slots(
        db,
        doctor_id,
        appointment_date,
    )

    available_slots = [
        slot
        for slot in slots
        if slot not in booked_slots
    ]

    return available_slots



def find_available_doctors(
    db: Session,
    specialty: Specialty,
    appointment_date: date,
):
    doctors = get_doctors_by_specialty(
        db,
        specialty,
    )

    available_doctors = []

    for doctor in doctors:

        slots = get_available_slots(
            db,
            doctor.id,
            appointment_date,
        )

        if slots:
            available_doctors.append(
                {
                    "doctor": doctor,
                    "slots": slots,
                }
            )

    return available_doctors