"""The only module permitted to import a model provider SDK.

Everything else in the system calls into here. FF-14 enforces that.
"""
import anthropic  # noqa: F401  provider SDK, permitted only in this module


def complete(capability: str, prompt: str) -> str:
    """Route, cache, meter and log a model call."""
    raise NotImplementedError("illustrative only")
