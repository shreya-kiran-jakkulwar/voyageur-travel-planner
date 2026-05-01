"""
Human-friendly output formatting for Voyageur trip plans.

All presentation logic lives here so that main.py and other
future interfaces (web, API) can swap formatters freely.
"""

from __future__ import annotations

import sys
from typing import Any

# ── ANSI helpers ─────────────────────────────────────────────────────────────

BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Use ASCII-safe characters to avoid Windows cp1252 encoding errors
RULE_CHAR = "-"
RULE = f"{DIM}{RULE_CHAR * 60}{RESET}"
SECTION_CHAR = "="
DAY_CHAR = "--"

# Currency symbol — use INR text if terminal can't render the symbol
_RUPEE = "INR "


def format_trip(data: dict[str, Any]) -> str:
    """
    Formats the full trip plan (brief + itinerary) into a
    human-readable, colour-coded string for terminal output.
    """
    lines: list[str] = []
    lines.append("")
    lines.append(RULE)
    lines.append(_section_header("TRIP BRIEF"))
    lines.append(RULE)
    lines.append(_format_brief(data.get("brief", {})))
    lines.append("")
    lines.append(RULE)
    lines.append(_section_header("ITINERARY"))
    lines.append(RULE)
    lines.append(_format_itinerary(data.get("itinerary", [])))
    return "\n".join(lines)


# ── Brief ────────────────────────────────────────────────────────────────────

_BRIEF_LABELS: list[tuple[str, str]] = [
    ("destination", "Destination"),
    ("duration_days", "Duration"),
    ("travelers", "Travelers"),
    ("budget_tier", "Budget Tier"),
    ("interests", "Interests"),
    ("pace", "Pace"),
    ("dietary_needs", "Dietary Needs"),
    ("notes", "Notes"),
]


def _format_brief(brief: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, label in _BRIEF_LABELS:
        value = brief.get(key, "-")
        display = _brief_value(key, value)
        lines.append(f"  {CYAN}{label:<16}{RESET} {display}")
    return "\n".join(lines)


def _brief_value(key: str, value: Any) -> str:
    """Produce a display string for a single brief field."""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "-"
    if key == "duration_days":
        return f"{value} day{'s' if value != 1 else ''}"
    if key == "travelers":
        return f"{value} traveler{'s' if value != 1 else ''}"
    if key == "budget_tier":
        return str(value).capitalize()
    if key == "pace":
        return str(value).capitalize()
    return str(value) if value else "-"


# ── Itinerary ────────────────────────────────────────────────────────────────

_TIME_SLOTS: list[tuple[str, str, str]] = [
    ("morning", "[Morning]", YELLOW),
    ("afternoon", "[Afternoon]", GREEN),
    ("evening", "[Evening]", MAGENTA),
]


def _format_itinerary(itinerary: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for day_data in itinerary:
        day_num = day_data.get("day", "?")
        lines.append(f"\n  {BOLD}{DAY_CHAR}  Day {day_num}  {DAY_CHAR}{RESET}")
        for slot_key, slot_label, colour in _TIME_SLOTS:
            slot = day_data.get(slot_key, {})
            lines.append(_format_slot(slot, slot_label, colour))
    return "\n".join(lines)


def _format_slot(slot: dict[str, Any], label: str, colour: str) -> str:
    """Format a single time-slot block (morning / afternoon / evening)."""
    activity = slot.get("activity", "-")
    location = slot.get("location", "-")
    duration = slot.get("duration_minutes", "-")
    cost = slot.get("estimated_cost_inr", 0)
    notes = slot.get("notes", "")

    duration_str = f"{duration} min" if isinstance(duration, int) else str(duration)
    cost_str = f"{_RUPEE}{cost:,}" if isinstance(cost, (int, float)) else str(cost)

    block = [
        f"\n    {colour}{BOLD}{label}{RESET}",
        f"      Activity  : {activity}",
        f"      Location  : {location}",
        f"      Duration  : {duration_str}",
        f"      Cost      : {cost_str}",
    ]
    if notes:
        block.append(f"      Notes     : {DIM}{notes}{RESET}")
    return "\n".join(block)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _section_header(title: str) -> str:
    return f"  {BOLD}{CYAN}>> {title}{RESET}"
