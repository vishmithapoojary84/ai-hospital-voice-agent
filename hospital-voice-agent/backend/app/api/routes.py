from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from livekit.api import AccessToken, VideoGrants
from app.config import settings

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


from fastapi import BackgroundTasks
from livekit import api

import json

async def dispatch_agent(
    room: str,
    language: str,
    stt_provider: str,
    llm_provider: str,
):
    lk = api.LiveKitAPI(
        settings.LIVEKIT_URL,
        settings.LIVEKIT_API_KEY,
        settings.LIVEKIT_API_SECRET,
    )

    try:
        try:
            metadata = json.dumps(
                {
                    "language": language,
                    "stt_provider": stt_provider,
                    "llm_provider": llm_provider,
                }
            )

            await lk.room.create_room(
                api.CreateRoomRequest(
                    name=room,
                    metadata=metadata,
                    empty_timeout=600,
                )
            )
            print("Room created")
        except Exception as e:
            print("Room already exists:", e)

        await lk.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name="hospital-agent",
                room=room,
            )
        )

        print("Agent dispatched!")

    finally:
        await lk.aclose()
@router.get("/token")
async def get_token(
    background_tasks: BackgroundTasks,
    identity: str = Query(...),
    room: str = Query(...),
    language: str = Query("english"),
    stt_provider: str = Query("deepgram"),
    llm_provider: str = Query("gemini"),
):
    token = (
        AccessToken(
            settings.LIVEKIT_API_KEY,
            settings.LIVEKIT_API_SECRET,
        )
        .with_identity(identity)
        .with_name(identity)
        .with_grants(
            VideoGrants(
                room_join=True,
                room=room,
            )
        )
        .to_jwt()
    )

    # Automatically dispatch the agent to this room
    background_tasks.add_task(
        dispatch_agent,
        room,
        language,
        stt_provider,
        llm_provider,
    )

    return {
        "token": token,
        "url": settings.LIVEKIT_URL,
    }