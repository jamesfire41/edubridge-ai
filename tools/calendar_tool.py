"""
EduBridge AI - Calendar Tool
In-memory session store. Replace with Google Calendar / DB in production.
"""

from core.state import Session


class CalendarTool:
    _sessions: dict[str, Session] = {}

    def add_session(self, session: Session):
        self._sessions[session.id] = session
        print(f"[CalendarTool] Session added: {session.id} @ {session.scheduled_at}")

    def get_session(self, session_id: str) -> Session | None:
        return self._sessions.get(session_id)

    def list_sessions(self, tutor_id: str = None, student_id: str = None) -> list[Session]:
        sessions = list(self._sessions.values())
        if tutor_id:
            sessions = [s for s in sessions if s.tutor_id == tutor_id]
        if student_id:
            sessions = [s for s in sessions if s.student_id == student_id]
        return sessions
