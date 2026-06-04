"""
EduBridge AI - Main Entry Point
Run with: python main.py --mode mock
"""

import argparse
from dotenv import load_dotenv

load_dotenv()

from core.state import EduBridgeState, IncomingMessage, MessageRole
from agents.orchestrator import edubridge_graph
from mock.whatsapp_mock import WhatsAppMock
from mock.mock_data import MOCK_TUTORS, MOCK_STUDENTS


def run_mock_demo():
    """Run an interactive mock demo in the terminal."""
    wa = WhatsAppMock()

    print("\n" + "█"*60)
    print("  🎓  EduBridge AI — Mock Demo Mode")
    print("  Powered by AMD ROCm + LangGraph + Ollama")
    print("█"*60)

    print("\n[Demo] Simulating tutor message...\n")

    # Simulate tutor creating a session
    tutor_msg = wa.receive(
        sender_id=MOCK_TUTORS[0]["phone"],
        content=(
            "Tolong buatkan jadwal belajar Matematika untuk Andi "
            "setiap Selasa dan Kamis jam 4 sore. Materi: Aljabar dasar. "
            "Metode: latihan soal interaktif."
        ),
        role=MessageRole.TUTOR,
    )

    # Build initial state
    state = EduBridgeState.initial(tutor_msg)
    state["active_tutor_id"]   = MOCK_TUTORS[0]["id"]
    state["active_student_id"] = MOCK_STUDENTS[0]["id"]

    print("\n[EduBridge] Running agent pipeline...\n")

    # Run through LangGraph
    result = edubridge_graph.invoke(state)

    # Deliver responses
    wa.deliver_outgoing(result.get("outgoing_messages", []))

    print("\n[Demo] Done! ✅")
    print(f"  Intent detected : {result.get('intent')}")
    print(f"  Messages sent   : {len(result.get('outgoing_messages', []))}")


def run_interactive():
    """Interactive REPL mode for manual testing."""
    wa = WhatsAppMock()

    print("\n🎓 EduBridge AI — Interactive Mode")
    print("Type your message as a tutor or student. Ctrl+C to quit.\n")

    while True:
        try:
            role_input = input("Role (tutor/student): ").strip().lower()
            role = MessageRole.TUTOR if role_input == "tutor" else MessageRole.STUDENT
            sender = MOCK_TUTORS[0]["phone"] if role == MessageRole.TUTOR else MOCK_STUDENTS[0]["phone"]
            content = input("Message: ").strip()

            if not content:
                continue

            msg   = wa.receive(sender_id=sender, content=content, role=role)
            state = EduBridgeState.initial(msg)

            result = edubridge_graph.invoke(state)
            wa.deliver_outgoing(result.get("outgoing_messages", []))

        except KeyboardInterrupt:
            print("\n\nBye! 👋")
            break


def main():
    parser = argparse.ArgumentParser(description="EduBridge AI")
    parser.add_argument(
        "--mode",
        choices=["mock", "interactive"],
        default="mock",
        help="Run mode: 'mock' for demo, 'interactive' for REPL",
    )
    args = parser.parse_args()

    if args.mode == "mock":
        run_mock_demo()
    elif args.mode == "interactive":
        run_interactive()


if __name__ == "__main__":
    main()
