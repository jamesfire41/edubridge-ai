"""
EduBridge AI - WhatsApp Mock Interface
Simulates WhatsApp messaging in the terminal for development and demo purposes.
Designed to be swapped with a real WhatsApp Business API adapter.
"""

import time
from datetime import datetime
from core.state import IncomingMessage, MessageRole


class WhatsAppMock:
    """
    Terminal-based simulation of WhatsApp conversations.
    Plug-and-play replacement for a real WA adapter.
    """

    def __init__(self):
        self.inbox: list[IncomingMessage] = []
        self.sent: list[dict] = []

    def receive(self, sender_id: str, content: str, role: MessageRole) -> IncomingMessage:
        """Simulate receiving a WhatsApp message."""
        msg = IncomingMessage(
            role=role,
            sender_id=sender_id,
            content=content,
            timestamp=datetime.now().isoformat(),
        )
        self.inbox.append(msg)
        self._print_incoming(msg)
        return msg

    def send(self, to: str, body: str):
        """Simulate sending a WhatsApp message."""
        record = {"to": to, "body": body, "sent_at": datetime.now().isoformat()}
        self.sent.append(record)
        self._print_outgoing(to, body)

    def deliver_outgoing(self, outgoing_messages: list[dict]):
        """Deliver all queued outgoing messages."""
        for msg in outgoing_messages:
            self.send(msg["to"], msg["body"])
            time.sleep(0.3)  # simulate delivery delay

    def _print_incoming(self, msg: IncomingMessage):
        role_emoji = {"tutor": "👨‍🏫", "student": "👤", "agent": "🤖", "system": "⚙️"}
        emoji = role_emoji.get(msg.role, "💬")
        print(f"\n{'─'*60}")
        print(f"{emoji}  [{msg.role.upper()}] {msg.sender_id}")
        print(f"    {msg.content}")
        print(f"    {msg.timestamp}")
        print(f"{'─'*60}")

    def _print_outgoing(self, to: str, body: str):
        print(f"\n{'═'*60}")
        print(f"🤖  [EDUBRIDGE → {to}]")
        for line in body.split("\n"):
            print(f"    {line}")
        print(f"{'═'*60}")
