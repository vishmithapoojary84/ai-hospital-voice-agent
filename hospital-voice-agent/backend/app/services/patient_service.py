from sqlalchemy.orm import Session

from app.database.patient import Patient


def get_patient_by_phone(
    db: Session,
    phone: str,
):
    return (
        db.query(Patient)
        .filter(
            Patient.phone == phone
        )
        .first()
    )

def create_patient(
    db: Session,
    name: str,
    phone: str,
):
    patient = Patient(
        name=name,
        phone=phone,
    )

    try:
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    except Exception:
        db.rollback()
        raise

    


def get_or_create_patient(
    db: Session,
    name: str,
    phone: str,
):
    patient = get_patient_by_phone(
        db,
        phone,
    )

    if patient is not None:
        return patient

    return create_patient(
        db,
        name,
        phone,
    )