#!/usr/bin/env python3
"""
Command-line chat interface for the Persona-Adaptive Support Agent.

    python cli.py
"""

import json
import traceback
from datetime import datetime

from src.agent import SupportAgent, AgentResponse
from src.handoff import HandoffGenerator


# ── ANSI Colors ──────────────────────────────────────────

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    GREEN   = "\033[92m"
    CYAN    = "\033[96m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"


PERSONA_COLORS = {
    "technical_expert": C.CYAN,
    "frustrated_user": C.YELLOW,
    "business_executive": C.MAGENTA,
}


def print_banner():
    print(f"""
{C.BOLD}{C.CYAN}
  ╔═══════════════════════════════════════════════════════════╗
  ║      CloudFlow — Persona-Adaptive Support Agent          ║
  ║      Type your message to get started.                   ║
  ║      Commands: /quit  /clear  /history  /json  /help     ║
  ╚═══════════════════════════════════════════════════════════╝
{C.RESET}""")


def print_response(resp: AgentResponse):
    color = PERSONA_COLORS.get(resp.persona, C.WHITE)

    print()
    print(f"  {C.DIM}── Detected Persona ──────────────────────────────{C.RESET}")
    print(f"  {color}{C.BOLD}{resp.persona_label}{C.RESET}"
          f"  {C.DIM}(confidence: {resp.persona_confidence:.0%}, "
          f"retrieval score: {resp.retrieval_score:.4f}){C.RESET}")

    if resp.sources:
        print(f"  {C.DIM}── Retrieved Sources ─────────────────────────────{C.RESET}")
        for s in resp.sources[:3]:
            src = s.get('source', 'unknown')
            sec = s.get('section', '')
            score = s.get('relevance_score', 0.0)
            print(f"  {C.DIM}• {src} — {sec} "
                  f"(score: {score:.4f}){C.RESET}")

    print(f"  {C.DIM}── Response ──────────────────────────────────────{C.RESET}")
    for line in resp.message.split("\n"):
        print(f"  {C.WHITE}{line}{C.RESET}")

    if resp.is_escalated:
        print()
        print(f"  {C.RED}{C.BOLD}  WARNING: ESCALATED TO HUMAN AGENT  {C.RESET}")
        if resp.escalation_summary:
            print()
            handoff = HandoffGenerator()
            print(handoff.format_display(resp.escalation_summary))

    print()


def main():
    print_banner()

    agent = SupportAgent()
    agent.initialize_knowledge_base()

    session_id = f"cli-{datetime.now().strftime('%H%M%S')}"
    show_json = False

    print(f"{C.DIM}  Session: {session_id}{C.RESET}")
    print(f"{C.DIM}  Tip: Use /clear between different test scenarios{C.RESET}")
    print(f"{C.DIM}  Ready. Type your message below.{C.RESET}")
    print()

    while True:
        try:
            user_input = input(f"{C.GREEN}{C.BOLD}  You > {C.RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{C.DIM}  Goodbye!{C.RESET}\n")
            break

        if not user_input:
            continue

        # ── Commands ────────────────────────────────────────
        if user_input.lower() == "/quit":
            print(f"\n{C.DIM}  Goodbye!{C.RESET}\n")
            break

        if user_input.lower() == "/clear":
            session_id = f"cli-{datetime.now().strftime('%H%M%S')}"
            agent.memory = __import__(
                'src.conversation_memory', fromlist=['ConversationMemory']
            ).ConversationMemory()
            print(f"  {C.DIM}New session: {session_id}{C.RESET}")
            print(f"  {C.DIM}Conversation history cleared.{C.RESET}\n")
            continue

        if user_input.lower() == "/history":
            history = agent.memory.get_history(session_id)
            if not history:
                print(f"  {C.DIM}No conversation history yet.{C.RESET}\n")
            else:
                print(f"\n  {C.DIM}Conversation history ({len(history)} turns):{C.RESET}")
                for turn in history:
                    role = turn["role"].upper()
                    content = turn["content"][:100]
                    print(f"    {C.DIM}{role}: {content}...{C.RESET}")
            print()
            continue

        if user_input.lower() == "/json":
            show_json = not show_json
            state = "ON" if show_json else "OFF"
            print(f"  {C.DIM}JSON output: {state}{C.RESET}\n")
            continue

        if user_input.lower() == "/help":
            print(f"""
  {C.BOLD}Commands:{C.RESET}
    {C.CYAN}/quit{C.RESET}     — Exit the application
    {C.CYAN}/clear{C.RESET}    — Start a new session (clear history)
    {C.CYAN}/history{C.RESET}  — Show conversation history
    {C.CYAN}/json{C.RESET}     — Toggle JSON response output
    {C.CYAN}/help{C.RESET}     — Show this help message
""")
            continue

        # ── Process message ─────────────────────────────────
        print(f"\n  {C.DIM}Processing...{C.RESET}")

        try:
            resp = agent.chat(user_input, session_id=session_id)
            print_response(resp)

            if show_json:
                print(f"  {C.DIM}── JSON Output ─────────────────────────────────{C.RESET}")
                print(json.dumps({
                    "persona": resp.persona,
                    "persona_label": resp.persona_label,
                    "confidence": resp.persona_confidence,
                    "retrieval_score": resp.retrieval_score,
                    "sources": resp.sources,
                    "is_escalated": resp.is_escalated,
                    "escalation_summary": resp.escalation_summary,
                }, indent=2, default=str))
                print()

        except Exception as e:
            print(f"\n  {C.RED}Error: {e}{C.RESET}")
            traceback.print_exc()
            print()


if __name__ == "__main__":
    main()