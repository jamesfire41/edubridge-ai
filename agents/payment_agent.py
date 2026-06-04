"""
EduBridge AI - Payment Agent
Manages tutoring packages, payment verification, and billing.
"""

from core.state import EduBridgeState, PaymentPackage, PaymentStatus
from core.llm_engine import get_llm_engine
from tools.payment_tool import PaymentTool


PACKAGES = [
    PaymentPackage("pkg_basic",   "Basic",   4,  150_000, PaymentStatus.UNPAID),
    PaymentPackage("pkg_pro",     "Pro",     8,  280_000, PaymentStatus.UNPAID),
    PaymentPackage("pkg_premium", "Premium", 16, 500_000, PaymentStatus.UNPAID),
]

PAYMENT_PROMPT = """You are EduBridge's payment assistant.

Available packages:
{packages}

User message: {message}
Intent: {intent}

Help the user with their payment request.
If buying a package, show the payment instructions clearly.
If checking payment, provide status update.
Keep it friendly and clear. Match the language of the message."""


class PaymentAgent:

    def __init__(self):
        self.tool = PaymentTool()

    def run(self, state: EduBridgeState) -> EduBridgeState:
        llm    = get_llm_engine().llm
        msg    = state["incoming_message"]
        intent = state.get("intent", "")

        print(f"[PaymentAgent] Handling intent: {intent}")

        packages_str = "\n".join(
            f"- {p.name}: {p.sessions_count} sesi / Rp {p.price_idr:,}"
            for p in PACKAGES
        )

        response = llm.invoke(PAYMENT_PROMPT.format(
            packages=packages_str,
            message=msg.content,
            intent=intent,
        ))

        if intent == "buy_package":
            # In real integration: generate payment link via Midtrans/Stripe
            payment_link = self.tool.generate_mock_payment_link(msg.sender_id)
            response += f"\n\n💳 Link pembayaran: {payment_link}"

        state["outgoing_messages"].append({
            "to": msg.sender_id,
            "body": response,
        })
        state["final_response"] = response
        return state
