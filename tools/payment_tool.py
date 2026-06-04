"""
EduBridge AI - Payment Tool
Mock payment link generator. Replace with Midtrans / Stripe in production.
"""

import uuid


class PaymentTool:

    def generate_mock_payment_link(self, user_id: str) -> str:
        token = str(uuid.uuid4())[:12].upper()
        return f"https://pay.edubridge.ai/mock/{token}?user={user_id}"

    def verify_payment(self, payment_id: str) -> dict:
        # In production: call Midtrans/Stripe webhook or polling
        return {
            "payment_id": payment_id,
            "status": "mock_paid",
            "amount": 150_000,
            "verified": True,
        }
