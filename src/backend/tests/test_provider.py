"""Provider: missing key is unavailable; timeout retries once."""

import pytest

from app.llm.provider import (
    LLMProviderAdapter,
    ProviderError,
    ProviderUnavailable,
)


def test_no_key_is_unavailable():
    adapter = LLMProviderAdapter(api_key="")
    assert adapter.is_available() is False
    with pytest.raises(ProviderUnavailable):
        adapter.generate("hello")


def test_timeout_retries_once_then_raises():
    calls = {"n": 0}

    def boom(_prompt, _system=None):
        calls["n"] += 1
        raise TimeoutError("slow")

    adapter = LLMProviderAdapter(api_key="", generate_fn=boom)
    assert adapter.is_available() is True
    with pytest.raises(ProviderError):
        adapter.generate("hello")
    assert calls["n"] == 2


def test_timeout_then_success_returns_text():
    calls = {"n": 0}

    def flaky(_prompt, _system=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise TimeoutError("slow")
        return "  ok  "

    adapter = LLMProviderAdapter(api_key="", generate_fn=flaky)
    assert adapter.generate("hello") == "ok"
    assert calls["n"] == 2
