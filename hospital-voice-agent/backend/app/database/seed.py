from datetime import time

from app.database.database import SessionLocal
from app.database.doctor import Doctor
from app.database.doctor_schedule import DoctorSchedule
from app.database.enums import Specialty, DayOfWeek


def seed_database():
    db = SessionLocal()

    try:
        # Don't seed twice
        if db.query(Doctor).first():
            print("Database already seeded.")
            return

        doctors = [
            Doctor(
                name="Dr. Priya",
                specialty=Specialty.DERMATOLOGIST,
            ),
            Doctor(
                name="Dr. Arun",
                specialty=Specialty.DERMATOLOGIST,
            ),
            Doctor(
                name="Dr. Meera",
                specialty=Specialty.CARDIOLOGIST,
            ),
            Doctor(
                name="Dr. Rahul",
                specialty=Specialty.ORTHOPEDIC,
            ),
            Doctor(
                name="Dr. Sneha",
                specialty=Specialty.GENERAL_PHYSICIAN,
            ),
            Doctor(
                name="Dr. Kiran",
                specialty=Specialty.GENERAL_PHYSICIAN,
            ),
            Doctor(
                name="Dr. Anjali",
                specialty=Specialty.PEDIATRICIAN,
            ),
            Doctor(
                name="Dr. Vikram",
                specialty=Specialty.NEUROLOGIST,
            ),
        ]

        db.add_all(doctors)
        db.commit()

        for doctor in doctors:
            db.refresh(doctor)

        working_days = [
            DayOfWeek.MONDAY,
            DayOfWeek.TUESDAY,
            DayOfWeek.WEDNESDAY,
            DayOfWeek.THURSDAY,
            DayOfWeek.FRIDAY,
        ]

        timings = {
            "Dr. Priya": (time(9, 0), time(13, 0)),
            "Dr. Arun": (time(14, 0), time(18, 0)),
            "Dr. Meera": (time(10, 0), time(16, 0)),
            "Dr. Rahul": (time(9, 0), time(17, 0)),
            "Dr. Sneha": (time(8, 0), time(14, 0)),
            "Dr. Kiran": (time(11, 0), time(17, 0)),
            "Dr. Anjali": (time(9, 0), time(15, 0)),
            "Dr. Vikram": (time(13, 0), time(18, 0)),
        }

        schedules = []

        for doctor in doctors:
            start_time, end_time = timings[doctor.name]

            for day in working_days:
                schedules.append(
                    DoctorSchedule(
                        doctor_id=doctor.id,
                        day_of_week=day,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )

        db.add_all(schedules)
        db.commit()

        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error while seeding database: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()