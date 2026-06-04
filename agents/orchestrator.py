"""
EduBridge AI - Orchestrator Agent
LangGraph state machine that routes messages to the appropriate sub-agents.
"""

from langgraph.graph import StateGraph, END
from core.state import EduBridgeState, MessageRole
from core.llm_engine import get_llm_engine
from agents.scheduler_agent import SchedulerAgent
from agents.learning_agent import LearningAgent
from agents.payment_agent import PaymentAgent
from agents.notifier_agent import NotifierAgent


# ─── Intent Classification ────────────────────────────────────────────────────

INTENT_PROMPT = """You are EduBridge AI, an autonomous education assistant.
Classify the user's intent into ONE of the following categories:
- schedule_session
- confirm_session
- cancel_session
- request_learning_material
- check_payment
- buy_package
- announce_live
- general_inquiry

User message: {message}

Respond with ONLY the intent label, nothing else."""


def classify_intent(state: EduBridgeState) -> EduBridgeState:
    """Use LLM to classify the incoming message intent."""
    llm = get_llm_engine().llm
    msg = state["incoming_message"].content
    intent = llm.invoke(INTENT_PROMPT.format(message=msg)).strip().lower()
    state["intent"] = intent
    print(f"[Orchestrator] Intent classified: {intent}")
    return state


# ─── Routing Logic ────────────────────────────────────────────────────────────

def route_by_intent(state: EduBridgeState) -> str:
    """Determine which agent should handle this request."""
    intent = state.get("intent", "general_inquiry")

    routing_map = {
        "schedule_session":         "scheduler",
        "confirm_session":          "scheduler",
        "cancel_session":           "scheduler",
        "request_learning_material":"learning",
        "check_payment":            "payment",
        "buy_package":              "payment",
        "announce_live":            "notifier",
        "general_inquiry":          "learning",
    }

    return routing_map.get(intent, "learning")


# ─── Agent Node Wrappers ──────────────────────────────────────────────────────

scheduler = SchedulerAgent()
learner   = LearningAgent()
payment   = PaymentAgent()
notifier  = NotifierAgent()


def run_scheduler(state: EduBridgeState) -> EduBridgeState:
    return scheduler.run(state)

def run_learning(state: EduBridgeState) -> EduBridgeState:
    return learner.run(state)

def run_payment(state: EduBridgeState) -> EduBridgeState:
    return payment.run(state)

def run_notifier(state: EduBridgeState) -> EduBridgeState:
    return notifier.run(state)


# ─── Build Graph ──────────────────────────────────────────────────────────────

def build_graph() -> StateGraph:
    graph = StateGraph(EduBridgeState)

    # Nodes
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("scheduler",       run_scheduler)
    graph.add_node("learning",        run_learning)
    graph.add_node("payment",         run_payment)
    graph.add_node("notifier",        run_notifier)

    # Entry point
    graph.set_entry_point("classify_intent")

    # Conditional routing after classification
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "scheduler": "scheduler",
            "learning":  "learning",
            "payment":   "payment",
            "notifier":  "notifier",
        }
    )

    # All agents terminate
    graph.add_edge("scheduler", END)
    graph.add_edge("learning",  END)
    graph.add_edge("payment",   END)
    graph.add_edge("notifier",  END)

    return graph.compile()


# Compiled graph singleton
edubridge_graph = build_graph()
