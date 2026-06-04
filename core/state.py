"""
EduBridge AI - Shared Agent State
Defines the central state object passed through the LangGraph pipeline.
"""

from typing import Annotated, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import operator


class MessageRole(str, Enum):
    TUTOR = "tutor"
    STUDENT = "student"
    AGENT = "agent"
    SYSTEM = "system"


class SessionStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


@dataclass
class IncomingMessage:
    role: MessageRole
    sender_id: str      # phone number or mock ID
    content: str
    timestamp: str


@dataclass
class Session:
    id: str
    tutor_id: str
    student_id: str
    subject: str
    method: str         # e.g., "interactive exercises", "lecture", "Q&A"
    scheduled_at: str   # ISO 8601
    duration_minutes: int = 60
    status: SessionStatus = SessionStatus.PENDING
    notes: str = ""


@dataclass
class PaymentPackage:
    id: str
    name: str           # e.g., "Basic", "Pro", "Premium"
    sessions_count: int
    price_idr: int
    status: PaymentStatus = PaymentStatus.UNPAID


# LangGraph state — all agents read/write this
class EduBridgeState(dict):
    """
    Central state object for the LangGraph orchestration graph.
    Each agent receives and returns a modified copy of this state.
    """

    # Incoming message triggering this pipeline run
    incoming_message: IncomingMessage

    # Resolved intent from the orchestrator
    intent: Optional[str]               # e.g., "schedule_session", "confirm_payment"

    # Active context
    active_tutor_id: Optional[str]
    active_student_id: Optional[str]
    active_session: Optional[Session]
    active_package: Optional[PaymentPackage]

    # Output messages queued for WhatsApp delivery
    outgoing_messages: list[dict]       # [{"to": phone, "body": text}]

    # Accumulated conversation history for LLM context
    conversation_history: list[dict]

    # Routing flags
    needs_scheduling: bool
    needs_learning_content: bool
    needs_payment_check: bool
    needs_notification: bool

    # Final agent response
    final_response: Optional[str]

    @classmethod
    def initial(cls, message: IncomingMessage) -> "EduBridgeState":
        return cls(
            incoming_message=message,
            intent=None,
            active_tutor_id=None,
            active_student_id=None,
            active_session=None,
            active_package=None,
            outgoing_messages=[],
            conversation_history=[],
            needs_scheduling=False,
            needs_learning_content=False,
            needs_payment_check=False,
            needs_notification=False,
            final_response=None,
        )
