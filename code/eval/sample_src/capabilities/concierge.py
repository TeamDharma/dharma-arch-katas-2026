"""Visitor concierge. Calls the gateway, never a provider directly."""
from gateway.model_gateway import complete


def answer(question: str) -> str:
    return complete("voice-concierge", question)
