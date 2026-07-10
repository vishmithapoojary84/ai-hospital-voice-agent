from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field

from app.database.enums import (
    Specialty,
    AppointmentStatus,
)


# ==========================================================
# Patient
# ==========================================================

class PatientCreate(BaseModel):
    name: str
    phone: str = Field(
        pattern=r"^\d{10}$",
        description="10-digit phone number",
    )


class PatientResponse(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Doctor
# ==========================================================

class DoctorResponse(BaseModel):
    id: int
    name: str
    specialty: Specialty
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Appointment
# ==========================================================

class AppointmentCreate(BaseModel):
    patient_name: str
    phone: str = Field(
        pattern=r"^\d{10}$",
        description="10-digit phone number",
    )
    doctor_id: int
    appointment_date: date
    appointment_time: time


class AppointmentResponse(BaseModel):
    id: int

    appointment_date: date
    appointment_time: time

    status: AppointmentStatus

    created_at: datetime
    updated_at: datetime

    doctor: DoctorResponse
    patient: PatientResponse

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
# Availability
# ==========================================================

class AvailabilityResponse(BaseModel):
    doctor_id: int
    doctor_name: str
    slots: list[time]


class AppointmentCancelResponse(BaseModel):
    message: str


class AppointmentHistoryResponse(BaseModel):
    id: int
    appointment_date: date
    appointment_time: time
    status: AppointmentStatus

    doctor: DoctorResponse

    model_config = ConfigDict(from_attributes=True)

class AppointmentRescheduleRequest(BaseModel):
    appointment_id: int
    appointment_date: date
    appointment_time: time


class AppointmentCancelRequest(BaseModel):
    appointment_id: int

