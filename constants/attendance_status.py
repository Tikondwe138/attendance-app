# constants/attendance_status.py

from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    TARDY = "tardy"

    @classmethod
    def list(cls):
        return [status.value for status in cls]

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value.lower() in cls.list()
