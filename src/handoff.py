import json
import re
from datetime import datetime, timezone
from langchain_core.messages import SystemMessage, HumanMessage

from .config import config
from .persona_detector import PERSONA_LABELS
from .llm import get_llm

SUMMARY_PROMPT = """You are generating a handoff summary for a human support agent.

Given the conversation, extract:
1. issue: One-sentence problem description
2. attempted_steps: List of troubleshooting steps already suggested
3. next_steps: Recommended action for the human agent

Respond with ONLY a valid JSON object (no markdown, no code blocks):
{"issue": "description", "attempted_steps": ["step1", "step2"], "next_steps": "recommendation"}"""


class HandoffGenerator:

    def __init__(self):
        self.llm = get_llm(temperature=0, max_tokens=512)

    
    def generate(self, user_message: str, persona: str, conversation_history: list, sources_used: list, escalation_reasons: list, priority: str, session_id: str,) -> dict:
        llm_summary = self._extract_summary(conversation_history, user_message)
        doc_names = list(set(s["source"] for s in sources_used))

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": session_id,
            "persona": PERSONA_LABELS.get(persona, persona),
            "issue": llm_summary.get("issue", user_message[:200]),
            "priority": priority,
            "escalation_reasons": escalation_reasons,
            "documents_used": doc_names,
            "attempted_steps": llm_summary.get("attempted_steps", []),
            "recommendation": llm_summary.get(
                "next_steps", "Review conversation and provide manual assistance."
            ),
            "conversation_history": conversation_history[-10:],
        }
    
    def _extract_summary(self, history: list, current_msg: str) -> dict:

        try:
            transcript = "\n".join(
                f"{h['role'].upper()}: {h['content']}" for h in history
            )

            response = self.llm.invoke([
                SystemMessage(content=SUMMARY_PROMPT),
                HumanMessage(
                    content=f"Conversation:\n{transcript}\n\nCurrent message:\n{current_msg}"
                ),
            ])

            content = response.content.strip()
            content = re.sub(r"```(?:json)?\s*", "", content)
            content = content.rstrip("`").strip()
            match = re.search(r"\{.*\}", content, re.DOTALL)

            if match:
                content = match.group(0)
            
            return json.loads(content)
        except Exception:
            return {
                "issue": current_msg[:200],
                "attempted_steps": [],
                "next_steps": "Review conversation and provide assistance.",
            }
    
    def format_display(self, summary: dict) -> str:

        lines = [
            "=" * 55,
            "  ESCALATION HANDOFF SUMMARY",
            "=" * 55,
            f"  Session:   {summary.get('session_id')}",
            f"  Persona:   {summary.get('persona')}",
            f"  Priority:  {summary.get('priority')}",
            "",
            f"  Issue: {summary.get('issue')}",
            "",
            "  Escalation Reasons:",
        ]

        for r in summary.get("escalation_reasons", []):
            lines.append(f"      - {r}")
        
        lines.append("")
        lines.append("  Documents Referenced:")

        for d in summary.get("documents_used", []):
            lines.append(f"      - {d}")

        lines.append("")
        lines.append("  Attempted Steps:")
        for s in summary.get("attempted_steps", []):
            lines.append(f"      - {s}")

        lines.append("")
        lines.append(f"  Recommended Next Steps:")
        lines.append(f"  {summary.get('recommendation')}")
        lines.append('=' * 55)

        return "\n".join(lines)

        
