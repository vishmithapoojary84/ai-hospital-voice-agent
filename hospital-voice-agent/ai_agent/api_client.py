import requests
from config import BACKEND_URL
from logger import logger

def _handle_http_error(e: requests.HTTPError) -> dict:
    try:
        if e.response is not None:
            data = e.response.json()
            if isinstance(data, dict) and "detail" in data:
                return {"error": data["detail"]}
    except Exception:
        pass
    return {"error": "Unable to complete the request."}


def get_availability(
    specialty: str,
    appointment_date: str,
):
    logger.info(
        f"GET /availability specialty={specialty} date={appointment_date}"
    )
    try:
        response = requests.get(
            f"{BACKEND_URL}/availability",
            params={
                "specialty": specialty,
                "appointment_date": appointment_date,
            },
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Availability Response: {result}")
        return result
    except requests.HTTPError as e:
        return _handle_http_error(e)
    except requests.ConnectionError:
        return {
            "error": "Hospital server is unavailable."
        }


def book_appointment(
    patient_name: str,
    phone: str,
    doctor_id: int,
    appointment_date: str,
    appointment_time: str,
):
    logger.info(
        f"POST /appointments/book doctor={doctor_id}"
    )
    try:
        response = requests.post(
            f"{BACKEND_URL}/appointments/book",
            json={
                "patient_name": patient_name,
                "phone": phone,
                "doctor_id": doctor_id,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
            },
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Booking Response: {result}")
        return result
    except requests.HTTPError as e:
        return _handle_http_error(e)
    except requests.ConnectionError:
        return {
            "error": "Hospital server is unavailable."
        }


def get_appointment_history(
    phone: str,
    status: str | None = None,
):
    logger.info(
        f"GET /appointments/history phone={phone}"
    )
    params = {
        "phone": phone,
    }
    if status is not None:
        status_map = {
            "scheduled": "Scheduled",
            "cancelled": "Cancelled",
            "completed": "Completed"
        }
        normalized_status = status_map.get(status.strip().lower(), status)
        params["status"] = normalized_status

    try:
        response = requests.get(
            f"{BACKEND_URL}/appointments/history",
            params=params,
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"History Response: {result}")
        return result
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            logger.info("History Response: [] (Patient not found 404)")
            return []
        return _handle_http_error(e)
    except requests.ConnectionError:
        return {
            "error": "Hospital server is unavailable."
        }


def cancel_appointment(
    appointment_id: int,
):
    logger.info(
        f"PATCH cancel appointment={appointment_id}"
    )
    try:
        response = requests.patch(
            f"{BACKEND_URL}/appointments/{appointment_id}/cancel",
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Cancel Response: {result}")
        return result
    except requests.HTTPError as e:
        return _handle_http_error(e)
    except requests.ConnectionError:
        return {
            "error": "Hospital server is unavailable."
        }


def reschedule_appointment(
    appointment_id: int,
    appointment_date: str,
    appointment_time: str,
):
    logger.info(
        f"PATCH reschedule appointment={appointment_id}"
    )
    try:
        response = requests.patch(
            f"{BACKEND_URL}/appointments/reschedule",
            json={
                "appointment_id": appointment_id,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time,
            },
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Reschedule Response: {result}")
        return result
    except requests.HTTPError as e:
        return _handle_http_error(e)
    except requests.ConnectionError:
        return {
            "error": "Hospital server is unavailable."
        }