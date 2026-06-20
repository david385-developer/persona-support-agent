from dataclasses import dataclass, field
from .config import config


@dataclass
class EscalationDecision:
    should_escalate: bool = False
    reasons: list = field(default_factory=list)
    priority: str = "P3"
    category: str = "general"


class EscalationEngine:


    def evaluate(
            self,
            user_message: str,
            retrieval_result: dict,
            turn_count: int = 0,
    ) -> EscalationDecision:
        
        decision = EscalationDecision()
        reasons = []
        lower_msg = user_message.lower()


        if not retrieval_result.get("has_relevant_context", False):
            reasons.append(
                f"No relevant knowledge base content found "
                f"(avg score: {retrieval_result.get('avg_score', 0):.2f}, "
                f"threshold: {config.SIMILARITY_THRESHOLD})"
            )
            decision.category = "unresolvable"

        avg_score = retrieval_result.get("avg_score", 1.0)

        if 0 < avg_score < config.SIMILARITY_THRESHOLD:
            reasons.append(f"Low retrieval confidence: {avg_score:.2f}")
        

        if turn_count >= config.MAX_TURNS_BEFORE_ESACALATION:
            reasons.append(
                f"Conversation reached {turn_count} turns without resolution"
            )
            decision.category = "prolonged"

        detected_topics = [
            kw for kw in config.SENSITIVE_KEYWORDS if kw in lower_msg
        ]

        if detected_topics:
            reasons.append(f"Sensitive topic(s) detected: {', '.join(detected_topics)}")

            decision.category = "sensitive"
            decision.priority = "P2"

        escalation_phrases = [
            "speak to human", "talk to a person", "human agent",
            "real person", "transfer to", "manager", "supervisor",
            "escalate", "someone who can actually help",
            "i want to talk to someone",
        ]

        if any(phrase in lower_msg for phrase in escalation_phrases):
            reasons.append("User explicitly requested escalation")
            decision.priority = "P2"
        
        frustration_phrases = [
            "not working", "still broken", "doesn't help",
            "tried that", "already done", "same issue",
            "not resolved", "didn't work", "still not fixed",
        ]

        frustration_count = sum(1 for p in frustration_phrases if p in lower_msg)
        if frustration_count >=2:
            reasons.append(
                f"Multiple frustration signals deteted ({frustration_count} matches)"
            )
        
        decision.should_escalate = len(reasons) >=1
        decision.reasons = reasons


        if len(reasons) >=3:
            decision.priority = "P1"
        elif len(reasons) >= 2 and decision.priority == "P3":
            decision.priority = "P2"
        
        return decision

