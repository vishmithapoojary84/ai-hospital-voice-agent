from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.enums import Specialty
from app.database.schemas import (
    AppointmentCreate,
    AppointmentResponse,
    AvailabilityResponse,
    DoctorResponse,
    AppointmentCancelResponse,
    AppointmentRescheduleRequest,
    AppointmentHistoryResponse,
    AppointmentStatus,
)
from app.services import (
    availability_service,
    booking_service,
    appointment_service,
    doctor_service,
)

router = APIRouter()


@router.get(
    "/doctors",
    response_model=list[DoctorResponse],
)
def get_doctors(
    specialty: Specialty,
    db: Session = Depends(get_db),
):
    return doctor_service.get_doctors_by_specialty(
        db,
        specialty,
    )

@router.get(
    "/availability",
    response_model=list[AvailabilityResponse],
)
def get_availability(
    specialty: Specialty,
    appointment_date: date,
    db: Session = Depends(get_db),
):
    available = availability_service.find_available_doctors(
        db,
        specialty,
        appointment_date,   
    )

    return [
        AvailabilityResponse(
            doctor_id=item["doctor"].id,
            doctor_name=item["doctor"].name,
            slots=item["slots"],
        )
            for item in available
    ]



@router.post(
    "/appointments/book",
    response_model=AppointmentResponse,
)
def book_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
):

    return booking_service.book_appointment(
        db=db,
        patient_name=appointment.patient_name,
        phone=appointment.phone,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,  
    )



@router.patch(
    "/appointments/{appointment_id}/cancel",
    response_model=AppointmentCancelResponse,
)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    return booking_service.cancel_appointment(
        db,
        appointment_id,
    )


@router.patch(
    "/appointments/reschedule",
    response_model=AppointmentResponse,
)
def reschedule_appointment(
    appointment: AppointmentRescheduleRequest,
    db: Session = Depends(get_db),
):

    return booking_service.reschedule_appointment(
        db=db,
        appointment_id=appointment.appointment_id,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
    )


@router.get(
    "/appointments/history",
    response_model=list[AppointmentHistoryResponse],
)
def appointment_history(
    phone: str,
    status: AppointmentStatus | None = None,
    db: Session = Depends(get_db),
):
    return appointment_service.get_patient_appointments(
        db=db,
        phone=phone,
        status=status,
    )