"""
OpenRouter API client for Voyageur.

Encapsulates all LLM communication: authentication, request construction,
response parsing, and retry logic. No other module should import `openai`
directly.
"""

from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

# ── Configuration ────────────────────────────────────────────────────────────

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-oss-120b:free"
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7
MAX_RETRIES = 1  # one automatic retry on JSON parse failure


class VoyageurClient:
    """Thin wrapper around the OpenAI SDK configured for OpenRouter."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise EnvironmentError(
                "OPENROUTER_API_KEY is not set or still contains the placeholder value.\n"
                "Please set a valid key in your .env file."
            )

        self._client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=api_key,
        )
        self._model = os.getenv("VOYAGEUR_MODEL", DEFAULT_MODEL)
        self._temperature = float(
            os.getenv("VOYAGEUR_TEMPERATURE", str(DEFAULT_TEMPERATURE))
        )
        self._max_tokens = int(
            os.getenv("VOYAGEUR_MAX_TOKENS", str(DEFAULT_MAX_TOKENS))
        )

    # ── Public API ───────────────────────────────────────────────────────────

    def generate_itinerary(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:
        """
        Send the prompts to the LLM and return parsed JSON.

        Retries once automatically if the first response is not valid JSON.
        Raises ``ValueError`` if both attempts fail.
        """
        raw_text = ""
        for attempt in range(1, MAX_RETRIES + 2):  # attempts 1 and 2
            raw_text = self._call_llm(system_prompt, user_prompt)
            parsed = self._try_parse_json(raw_text)
            if parsed is not None:
                return parsed

            if attempt <= MAX_RETRIES:
                print(
                    f"\n[!] Response was not valid JSON (attempt {attempt}). "
                    "Retrying..."
                )

        raise ValueError(
            "Failed to obtain valid JSON from the model after "
            f"{MAX_RETRIES + 1} attempt(s).\n"
            f"Last raw response:\n{raw_text}"
        )

    # ── Internals ────────────────────────────────────────────────────────────

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Execute a single chat-completion request and return raw text."""
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        return content if content is not None else ""

    @staticmethod
    def _try_parse_json(text: str) -> dict[str, Any] | None:
        """
        Attempt to parse ``text`` as JSON.

        Handles common LLM quirks like wrapping JSON in markdown code fences.
        Returns ``None`` on failure instead of raising.
        """
        cleaned = text.strip()

        # Strip markdown code fences if present
        if cleaned.startswith("```"):
            # Remove opening fence (```json or ```)
            first_newline = cleaned.index("\n")
            cleaned = cleaned[first_newline + 1 :]
            # Remove closing fence
            if cleaned.endswith("```"):
                cleaned = cleaned[: -3].strip()

        try:
            return json.loads(cleaned)
        except (json.JSONDecodeError, ValueError):
            return None
