"""
Defines the expected JSON schema for trip planning responses.

This schema is injected into the LLM prompt to enforce structured output.
It is kept separate so it can be versioned, extended, or swapped independently.
"""

TRIP_SCHEMA = """{
  "brief": {
    "destination": "string — city/region and country",
    "duration_days": "int — total number of days",
    "travelers": "int — number of travelers",
    "budget_tier": "budget | mid | luxury",
    "interests": ["string — e.g. history, food, adventure"],
    "pace": "relaxed | moderate | packed",
    "dietary_needs": ["string — e.g. vegetarian, halal, none"],
    "notes": "string — any extra observations"
  },
  "itinerary": [
    {
      "day": "int — day number starting from 1",
      "morning": {
        "activity": "string",
        "location": "string — specific venue or area",
        "duration_minutes": "int",
        "estimated_cost_inr": "int — cost in Indian Rupees",
        "notes": "string"
      },
      "afternoon": {
        "activity": "string",
        "location": "string",
        "duration_minutes": "int",
        "estimated_cost_inr": "int",
        "notes": "string"
      },
      "evening": {
        "activity": "string",
        "location": "string",
        "duration_minutes": "int",
        "estimated_cost_inr": "int",
        "notes": "string"
      }
    }
  ]
}"""
