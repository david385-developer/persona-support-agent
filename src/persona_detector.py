"""
Persona Detection Module

Detects which type of customer is talking to us:
- Technical Expert: Uses jargon, asks for details
- Frustrated User: Emotional, negative language
- Business Executive: Outcome-focused, concise

Uses two methods:
1. LLM classification (via Groq)
2. Keyword heuristics (pure Python fallback)
"""

import json
import re
from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage

from .config import config
from .llm import get_llm

Persona = Literal["technical_expert", "frustrated_user", "business_executive"]

PERSONA_LABELS = {
    "technical_expert": "Technical Expert",
    "frustrated_user": "Frustrated User",
    "business_executive": "Business Executive",
}

# ── Keyword lists for heuristic detection ──────────────

TECHNICAL_KEYWORDS = [
    "api", "endpoint", "http", "status code", "json", "sdk",
    "oauth", "saml", "sso", "webhook", "ssl", "dns", "payload",
    "authentication", "bearer", "token", "jwt", "cors",
    "header", "request id", "rate limit", "latency", "timeout",
    "401", "403", "404", "429", "500", "log", "debug",
    "configuration", "deploy", "database", "query", "schema",
    "migration", "regex", "curl", "postman", "graphql",
]

FRUSTRATED_KEYWORDS = [
    "frustrated", "angry", "terrible", "awful", "worst", "hate",
    "unacceptable", "ridiculous", "useless", "broken",
    "nothing works", "tried everything", "fed up",
    "waste of time", "still not working", "keeps happening",
    "disappointed", "furious", "pathetic", "scam",
    "again and again", "nobody helps", "so annoying",
]

BUSINESS_KEYWORDS = [
    "roi", "revenue", "cost", "budget", "stakeholder",
    "kpi", "metric", "impact", "operations", "downtime cost",
    "business continuity", "sla", "compliance", "enterprise",
    "timeline", "roadmap", "bottom line", "productivity",
    "efficiency", "when will", "business impact", "report",
    "quarterly", "executive", "strategic", "scalability",
]


def heuristic_scores(message: str) -> dict[str, float]:
    """Score message against keyword lists. Returns 0.0-1.0 per persona."""
    lower = message.lower()

    def count_matches(keywords):
        hits = sum(1 for kw in keywords if kw in lower)
        return min(hits / 4.0, 1.0)

    exclamations = message.count("!")
    frustration_boost = min(exclamations * 0.1, 0.3)

    return {
        "technical_expert": count_matches(TECHNICAL_KEYWORDS),
        "frustrated_user": count_matches(FRUSTRATED_KEYWORDS) + frustration_boost,
        "business_executive": count_matches(BUSINESS_KEYWORDS),
    }


def clean_json_response(content: str) -> str:
    """Extract JSON from LLM response, handling markdown wrapping."""
    content = content.strip()
    content = re.sub(r"```(?:json)?\s*", "", content)
    content = content.rstrip("`").strip()
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        return match.group(0)
    return content


PERSONA_DETECTION_PROMPT = """You are a customer persona classifier for a SaaS product called CloudFlow.

Classify the customer message into exactly ONE of these personas:

1. technical_expert — Uses technical jargon (API, endpoint, SDK, logs, configuration). Asks for specific error details, API documentation, or root cause analysis.

2. frustrated_user — Uses emotional or negative language. Expresses anger, impatience, or repeated complaints. Says things like "nothing works," "tried everything," "still broken."

3. business_executive — Focuses on business outcomes, ROI, timeline, impact on operations. Wants concise answers. Uses business terminology like SLA, KPI, stakeholders.

Respond with ONLY a JSON object (no markdown, no code blocks, no explanation before or after):
{"persona": "technical_expert", "confidence": 0.85, "reasoning": "one sentence explanation"}"""


class PersonaDetector:
    """Detects customer persona using LLM + keyword heuristics."""

    def __init__(self):
        self.llm = get_llm(temperature=0)

    def detect(self, message: str) -> dict:
        """
        Detect persona from user message.

        Returns:
            {
                "persona": "technical_expert" | "frustrated_user" | "business_executive",
                "label": "Technical Expert" | "Frustrated User" | "Business Executive",
                "confidence": float,
                "reasoning": str,
                "method": "llm" | "combined" | "heuristic"
            }
        """
        llm_result = self._llm_classify(message)
        heuristic = heuristic_scores(message)

        if llm_result:
            llm_persona = llm_result.get("persona", "technical_expert")
            llm_conf = llm_result.get("confidence", 0.5)

            if llm_persona not in PERSONA_LABELS:
                llm_persona = "technical_expert"
                llm_conf = 0.5

            if llm_conf >= 0.8:
                return {
                    "persona": llm_persona,
                    "label": PERSONA_LABELS[llm_persona],
                    "confidence": llm_conf,
                    "reasoning": llm_result.get("reasoning", ""),
                    "method": "llm",
                }

            # Combine LLM + heuristic
            combined = {}
            for p in PERSONA_LABELS:
                llm_score = llm_conf if p == llm_persona else (1 - llm_conf) / 2
                combined[p] = 0.6 * llm_score + 0.4 * heuristic[p]

            best = max(combined, key=combined.get)
            return {
                "persona": best,
                "label": PERSONA_LABELS[best],
                "confidence": round(combined[best], 4),
                "reasoning": f"Combined: {llm_result.get('reasoning', '')}",
                "method": "combined",
            }

        # Fallback: heuristics only
        best = max(heuristic, key=heuristic.get)
        return {
            "persona": best,
            "label": PERSONA_LABELS[best],
            "confidence": round(heuristic[best], 4),
            "reasoning": "Heuristic classification (LLM unavailable)",
            "method": "heuristic",
        }

    def _llm_classify(self, message: str) -> dict | None:
        """Call LLM for persona classification. Returns None on failure."""
        try:
            response = self.llm.invoke([
                SystemMessage(content=PERSONA_DETECTION_PROMPT),
                HumanMessage(content=f'Customer message:\n"{message}"'),
            ])
            content = clean_json_response(response.content)
            result = json.loads(content)
            if "persona" in result:
                return result
            return None
        except Exception as e:
            print(f"  [Persona] LLM classification failed: {e}")
            return None