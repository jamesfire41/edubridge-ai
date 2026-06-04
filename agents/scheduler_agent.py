"""
EduBridge AI - Scheduler Agent
Handles session creation, confirmation, and cancellation.
"""

from core.state import EduBridgeState, Session, SessionStatus
from core.llm_engine import get_llm_engine
from tools.calendar_tool import CalendarTool
import uuid
from datetime import datetime


SCHEDULER_PROMPT = """You are EduBridge's scheduling assistant.
Extract scheduling details from the message and respond in a friendly, clear way.
Current time: {now}

Message: {message}
Intent: {intent}

If scheduling a new session, confirm the details and ask for student confirmation.
If confirming, finalize the session.
If cancelling, acknowledge and offer to reschedule.

Keep response concise and in the same language as the message."""


class SchedulerAgent:

    def __init__(self):
        self.calendar = CalendarTool()

    def run(self, state: EduBridgeState) -> EduBridgeState:
        llm    = get_llm_engine().llm
        msg    = state["incoming_message"]
        intent = state.get("intent", "")

        print(f"[SchedulerAgent] Handling intent: {intent}")

        # Generate LLM response
        response = llm.invoke(SCHEDULER_PROMPT.format(
            now=datetime.now().strftime("%Y-%m-%d %H:%M"),
            message=msg.content,
            intent=intent,
        ))

        # If new session requested, create a pending session object
        if intent == "schedule_session":
            session = Session(
                id=str(uuid.uuid4())[:8],
                tutor_id=state.get("active_tutor_id", "tutor_001"),
                student_id=state.get("active_student_id", "student_001"),
                subject="[Extracted from message]",
                method="[Extracted from message]",
                scheduled_at="[Extracted from message]",
                status=SessionStatus.PENDING,
            )
            state["active_session"] = session
            self.calendar.add_session(session)

        elif intent == "confirm_session":
            if state.get("active_session"):
                state["active_session"].status = SessionStatus.CONFIRMED

        elif intent == "cancel_session":
            if state.get("active_session"):
                state["active_session"].status = SessionStatus.CANCELLED

        # Queue outgoing message
        state["outgoing_messages"].append({
            "to": msg.sender_id,
            "body": response,
        })
        state["final_response"] = response
        return state
