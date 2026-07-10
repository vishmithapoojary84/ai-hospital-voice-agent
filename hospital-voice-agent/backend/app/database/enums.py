from enum import Enum


class Specialty(str, Enum):
    DERMATOLOGIST = "Dermatologist"
    CARDIOLOGIST = "Cardiologist"
    PEDIATRICIAN = "Pediatrician"
    ORTHOPEDIC = "Orthopedic"
    GENERAL_PHYSICIAN = "General Physician"
    NEUROLOGIST = "Neurologist"
    GYNECOLOGIST = "Gynecologist"


class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"