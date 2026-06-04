"""
EduBridge AI - Mock Data
Sample tutors, students, and sessions for development/demo.
"""

MOCK_TUTORS = [
    {
        "id": "tutor_001",
        "name": "Pak Budi",
        "phone": "+6281234567890",
        "subjects": ["Matematika", "Fisika"],
        "method": "latihan soal interaktif dengan penjelasan bertahap",
    },
    {
        "id": "tutor_002",
        "name": "Bu Sari",
        "phone": "+6289876543210",
        "subjects": ["Bahasa Inggris", "Bahasa Indonesia"],
        "method": "percakapan langsung dan koreksi real-time",
    },
]

MOCK_STUDENTS = [
    {"id": "student_001", "name": "Andi",  "phone": "+6281111111111"},
    {"id": "student_002", "name": "Citra", "phone": "+6282222222222"},
    {"id": "student_003", "name": "Dimas", "phone": "+6283333333333"},
]

MOCK_SESSIONS = [
    {
        "id": "sess_001",
        "tutor_id": "tutor_001",
        "student_id": "student_001",
        "subject": "Matematika - Aljabar",
        "scheduled_at": "2025-07-10T16:00:00",
        "status": "confirmed",
    }
]

# Quick lookup helpers
TUTOR_BY_ID    = {t["id"]: t for t in MOCK_TUTORS}
STUDENT_BY_ID  = {s["id"]: s for s in MOCK_STUDENTS}
TUTOR_BY_PHONE = {t["phone"]: t for t in MOCK_TUTORS}
