"""
Builds the system and user prompts for itinerary generation.

The system prompt locks the model into strict JSON output mode,
while the user prompt injects the traveler's free-text description.
"""

from schemas.trip_schema import TRIP_SCHEMA


def build_system_prompt() -> str:
    """
    Returns the system prompt that instructs the LLM to act as a
    travel planning assistant and produce strictly valid JSON.
    """
    return f"""You are Voyageur, an expert travel planning assistant.

Your job is to take a traveler's free-text trip description and produce a
structured travel plan as **pure JSON** — no markdown, no commentary, no
code fences, no extra text before or after the JSON object.

## Rules

1. **Output ONLY valid JSON** matching the schema below. Nothing else.
2. If the user does not specify a value (e.g. number of travelers, budget),
   infer a sensible default and note your assumption in the "notes" field.
3. The length of the "itinerary" array MUST equal "duration_days".
4. All costs must be realistic estimates in Indian Rupees (INR).
5. Durations must be realistic (e.g. a museum visit ≈ 90–120 min).
6. "budget_tier" must be exactly one of: budget, mid, luxury.
7. "pace" must be exactly one of: relaxed, moderate, packed.
8. Do NOT wrap the JSON in markdown code fences or add any explanation.

## Required JSON Schema

{TRIP_SCHEMA}
"""


def build_user_prompt(user_input: str) -> str:
    """
    Wraps the traveler's raw description into the user message.
    """
    return f"""Here is the traveler's trip description:

\"{user_input}\"

Produce the trip plan as strict JSON now."""
