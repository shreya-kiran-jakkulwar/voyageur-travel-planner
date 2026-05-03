"""
Voyageur — AI-powered travel planning assistant.

Entry point: orchestrates user input -> LLM call -> formatted output.
Run with:  python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so sibling packages resolve
# regardless of the working directory used to invoke the script.
_PROJECT_ROOT = Path(__file__).resolve().parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv

# Load environment variables from .env (must happen before client init)
load_dotenv(dotenv_path=_PROJECT_ROOT / ".env")

from client import VoyageurClient
from prompts.itinerary_prompt import build_system_prompt, build_user_prompt
from utils.formatter import format_trip

# ── ANSI helpers ─────────────────────────────────────────────────────────────
BOLD = "\033[1m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"


def main() -> None:
    """Top-level orchestrator for the CLI workflow."""
    
    # Force UTF-8 encoding for standard output on Windows
    if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    # 1. Greeting
    print(f"\n{BOLD}{CYAN}Welcome to Voyageur{RESET}")
    print(f"{CYAN}   Your AI-powered travel planner{RESET}\n")

    # 2. Collect user input
    try:
        user_input = input(f"{BOLD}Describe your trip:{RESET} ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nGoodbye!")
        return

    if not user_input:
        print(f"{RED}No trip description provided. Exiting.{RESET}")
        return

    # 3. Build prompts
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(user_input)

    # 4. Call the LLM via OpenRouter
    print(f"\nPlanning your trip -- this may take a moment...\n")
    try:
        client = VoyageurClient()
        trip_data = client.generate_itinerary(system_prompt, user_prompt)
    except EnvironmentError as exc:
        print(f"{RED}Configuration error:{RESET} {exc}")
        sys.exit(1)
    except ValueError as exc:
        print(f"{RED}Generation error:{RESET} {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"{RED}Unexpected error:{RESET} {exc}")
        sys.exit(1)

    # 5. Format and display
    output = format_trip(trip_data)
    print(output)
    print()


if __name__ == "__main__":
    main()
