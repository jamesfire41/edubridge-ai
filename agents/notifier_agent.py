"""
EduBridge AI - Notifier Agent
Broadcasts live session announcements and reminders to students.
"""

from core.state import EduBridgeState
from core.llm_engine import get_llm_engine
from mock.mock_data import MOCK_STUDENTS


ANNOUNCE_PROMPT = """You are EduBridge's announcement assistant.
A tutor wants to announce a live online session.

Tutor message: {message}

Generate a clear, exciting announcement message for students.
Include all relevant details (topic, time, link if mentioned).
Keep it short and engaging. Match the language of the tutor's message."""


class NotifierAgent:

    def run(self, state: EduBridgeState) -> EduBridgeState:
        llm = get_llm_engine().llm
        msg = state["incoming_message"]

        print("[NotifierAgent] Broadcasting announcement")

        announcement = llm.invoke(ANNOUNCE_PROMPT.format(message=msg.content))

        # In real mode: blast to all subscribed students via WA API
        # In mock mode: queue messages to all mock students
        for student in MOCK_STUDENTS:
            state["outgoing_messages"].append({
                "to": student["id"],
                "body": f"📢 *Live Session Alert!*\n\n{announcement}",
            })

        # Confirm to tutor
        state["outgoing_messages"].append({
            "to": msg.sender_id,
            "body": f"✅ Pengumuman berhasil dikirim ke {len(MOCK_STUDENTS)} murid!",
        })

        state["final_response"] = announcement
        return state
