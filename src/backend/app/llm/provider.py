"""Gemini adapter. Timeout / 429 retry once, then the caller uses templates."""

from __future__ import annotations

from collections.abc import Callable

from app.core.config import get_settings

GenerateFn = Callable[[str, str | None], str]


class ProviderError(Exception):
    """Provider was called and failed after the bounded retry."""


class ProviderUnavailable(ProviderError):
    """No key, or the SDK is missing. Skip Stage 1 / Stage 3."""


def _is_retryable(exc: BaseException) -> bool:
    if isinstance(exc, (TimeoutError, ConnectionError)):
        return True
    code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    if code in (408, 429, 500, 502, 503, 504):
        return True
    name = type(exc).__name__.lower()
    return "timeout" in name or "rate" in name or "unavailable" in name


class LLMProviderAdapter:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        timeout_ms: int | None = None,
        generate_fn: GenerateFn | None = None,
    ) -> None:
        settings = get_settings()
        self.api_key = settings.GEMINI_API_KEY if api_key is None else api_key
        self.model = model or settings.GEMINI_MODEL
        self.timeout_ms = (
            settings.GEMINI_TIMEOUT_MS if timeout_ms is None else timeout_ms
        )
        self._generate_fn = generate_fn

    def is_available(self) -> bool:
        if self._generate_fn is not None:
            return True
        return bool(self.api_key)

    def generate(self, prompt: str, system: str | None = None) -> str:
        if not self.is_available():
            raise ProviderUnavailable("GEMINI_API_KEY is not set")

        last: BaseException | None = None
        for attempt in range(2):
            try:
                text = self._call(prompt, system)
                if not text or not text.strip():
                    raise ProviderError("Provider returned empty text")
                return text.strip()
            except ProviderUnavailable:
                raise
            except Exception as exc:
                last = exc
                if attempt == 0 and _is_retryable(exc):
                    continue
                if _is_retryable(exc):
                    raise ProviderError(str(exc)) from exc
                raise ProviderError(str(exc)) from exc
        raise ProviderError(str(last)) from last

    def _call(self, prompt: str, system: str | None) -> str:
        if self._generate_fn is not None:
            return self._generate_fn(prompt, system)
        return self._gemini_call(prompt, system)

    def _gemini_call(self, prompt: str, system: str | None) -> str:
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise ProviderUnavailable(
                "google-genai is not installed"
            ) from exc

        client = genai.Client(
            api_key=self.api_key,
            http_options=types.HttpOptions(
                timeout=self.timeout_ms,
                retry_options=types.HttpRetryOptions(attempts=1),
            ),
        )
        config_kwargs: dict = {"temperature": 0.2}
        if system:
            config_kwargs["system_instruction"] = system
        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        return (response.text or "").strip()
