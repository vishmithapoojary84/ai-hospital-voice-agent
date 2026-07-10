from datetime import date, datetime, time

from fastapi import HTTPException


def validate_appointment_datetime(
    appointment_date: date,
    appointment_time: time,
):
    if appointment_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Appointment date cannot be in the past.",
        )

    if (
        appointment_date == date.today()
        and appointment_time <= datetime.now().time()
    ):
        raise HTTPException(
            status_code=400,
            detail="Appointment time has already passed.",
        )