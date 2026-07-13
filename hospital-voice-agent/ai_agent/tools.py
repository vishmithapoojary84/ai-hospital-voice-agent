import asyncio
from api_client import (
    get_availability,
    book_appointment,
    get_appointment_history,
    cancel_appointment,
    reschedule_appointment,
)
from logger import logger

async def availability_tool(
    specialty: str,
    appointment_date: str,
):
    """
    Retrieve available doctors and appointment slots.

    Arguments:
        specialty: Doctor specialty exactly matching the hospital values.
        appointment_date: Date in YYYY-MM-DD format.

    Returns:
        Doctors with their available appointment slots.
    """
    logger.info(f"availability_tool raw call: {locals()}")
    logger.info(
        f"Availability Tool | specialty={specialty} date={appointment_date}"
    )
    return await asyncio.to_thread(
        get_availability,
        specialty,
        appointment_date,
    )


async def booking_tool(
    patient_name: str,
    phone: str,
    doctor_id: int,
    appointment_date: str,
    appointment_time: str,
):
    """
    Book a hospital appointment.

    Call this tool only after the patient has:
    - selected a doctor
    - selected an appointment slot
    - confirmed they want to book
    - provided their name
    - provided their phone number
    """
    logger.info(
        f"Booking Tool | "
        f"name={patient_name} "
        f"phone={phone} "
        f"doctor={doctor_id} "
        f"date={appointment_date} "
        f"time={appointment_time}"
    )

    if not patient_name or not patient_name.strip():
        return {
            "success": False,
            "message": "Patient name is required. Please ask the patient for their full name."
        }

    if not phone or not phone.strip():
        return {
            "success": False,
            "message": "Phone number is required. Please ask the patient for their phone number."
        }

    phone = phone.strip()

    if not phone.isdigit() or len(phone) != 10:
        return {
            "success": False,
            "message": "Please provide a valid 10-digit phone number."
        }

    return await asyncio.to_thread(
        book_appointment,
        patient_name,
        phone,
        doctor_id,
        appointment_date,
        appointment_time,
    )


async def history_tool(
    phone: str,
    status: str | None = None,
):
    """
    Retrieve a patient's appointment history.

    Status may be:
    - Scheduled
    - Cancelled
    - Completed

    Leave status empty to retrieve all appointments.
    """
    logger.info(f"history_tool raw call: {locals()}")
    logger.info(
        f"History Tool | phone={phone}"
    )

    if not phone or not phone.strip():
        return {
            "error": "Phone number is required. Please ask the patient for their phone number."
        }

    phone = phone.strip()

    if not phone.isdigit() or len(phone) != 10:
        return {
            "error": "Please provide a valid 10-digit phone number."
        }

    return await asyncio.to_thread(
        get_appointment_history,
        phone,
        status,
    )


async def cancel_tool(
    appointment_id: int,
):
    """
    Cancel an appointment.
    
    Call this tool only after the patient has:
    - provided their phone number
    - identified the appointment to cancel
    - confirmed they want to cancel
    """
    logger.info(f"cancel_tool raw call: {locals()}")
    logger.info(
        f"Cancel Tool | appointment_id={appointment_id}"
    )

    if appointment_id is None:
        return {
            "error": "Appointment ID is required."
        }

    return await asyncio.to_thread(
        cancel_appointment,
        appointment_id,
    )


async def reschedule_tool(
    appointment_id: int,
    appointment_date: str,
    appointment_time: str,
):
    """
    Reschedule an appointment.
    
    Call this tool only after the patient has:
    - provided their phone number
    - identified the appointment to reschedule
    - selected a new date
    - selected a new slot
    - confirmed they want to reschedule
    """
    logger.info(f"reschedule_tool raw call: {locals()}")
    logger.info(
        f"Reschedule Tool | appointment_id={appointment_id} new_date={appointment_date} new_time={appointment_time}"
    )

    if appointment_id is None:
        return {
            "error": "Appointment ID is required."
        }

    return await asyncio.to_thread(
        reschedule_appointment,
        appointment_id,
        appointment_date,
        appointment_time,
    )