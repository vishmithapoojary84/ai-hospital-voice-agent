from sqlalchemy.orm import Session

from app.database.doctor import Doctor
from app.database.enums import Specialty


def get_doctors_by_specialty(
    db: Session,
    specialty: Specialty
):
    return (
        db.query(Doctor)
        .filter(
            Doctor.specialty == specialty,
            Doctor.is_active == True
        )
        .all()
    )

def get_doctor_by_id(
    db: Session,
    doctor_id: int
):
    return (
        db.query(Doctor)
        .filter(
            Doctor.id == doctor_id
        )
        .first()
    )