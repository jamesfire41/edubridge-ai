"""
EduBridge AI - Learning Agent
Generates and delivers personalized learning content based on tutor's curriculum.
"""

from core.state import EduBridgeState
from core.llm_engine import get_llm_engine


LEARNING_PROMPT = """You are EduBridge's learning assistant.
A tutor has set up a learning session with the following configuration:

Subject: {subject}
Teaching Method: {method}
Additional Notes: {notes}

Student message: {message}

Generate a helpful, engaging response appropriate for the subject and method.
Keep it conversational and encouraging. Match the language of the student's message."""


GENERAL_PROMPT = """You are EduBridge AI, a friendly education assistant.
Help the user with their question: {message}
Be concise, friendly, and helpful."""


class LearningAgent:

    def run(self, state: EduBridgeState) -> EduBridgeState:
        llm = get_llm_engine().llm
        msg = state["incoming_message"]
        session = state.get("active_session")

        print("[LearningAgent] Generating learning content")

        if session:
            prompt = LEARNING_PROMPT.format(
                subject=session.subject,
                method=session.method,
                notes=session.notes,
                message=msg.content,
            )
        else:
            prompt = GENERAL_PROMPT.format(message=msg.content)

        response = llm.invoke(prompt)

        state["outgoing_messages"].append({
            "to": msg.sender_id,
            "body": response,
        })
        state["final_response"] = response
        return state
