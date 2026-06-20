

import uuid
from dataclasses import dataclass
from typing import Optional

from .config import config
from .persona_detector import PersonaDetector, PERSONA_LABELS
from .knowledge_base import KnowledgeBase
from .rag_pipeline import RAGPipeline
from .response_generator import ResponseGenerator
from .escalation import EscalationEngine
from .handoff import HandoffGenerator
from .conversation_memory import ConversationMemory


@dataclass
class AgentResponse:
    
    message: str
    persona: str
    persona_label: str
    persona_confidence: float
    sources: list
    retrieval_score: float
    is_escalated: bool
    escalation_summary: Optional[dict] = None
    session_id: str = ""


class SupportAgent:
   

    def __init__(self):
        print("Initializing Support Agent...")
        self.persona_detector = PersonaDetector()
        self.knowledge_base = KnowledgeBase()
        self.rag_pipeline = RAGPipeline(self.knowledge_base)
        self.response_generator = ResponseGenerator()
        self.escalation_engine = EscalationEngine()
        self.handoff_generator = HandoffGenerator()
        self.memory = ConversationMemory()
        print("Agent ready.\n")

    def initialize_knowledge_base(self):
        
        print("Building knowledge base...")
        self.knowledge_base.build_vector_store()
        print("Knowledge base ready.\n")

    def chat(self, user_message: str, session_id: str = None) -> AgentResponse:
       
        session_id = session_id or str(uuid.uuid4())[:8]

       
        self.memory.add_user_message(session_id, user_message)
        history = self.memory.get_history(session_id)
        turn_count = self.memory.get_turn_count(session_id)

        
        persona_result = self.persona_detector.detect(user_message)
        persona = persona_result["persona"]
        self.memory.update_persona(
            session_id, persona, persona_result["confidence"]
        )

        print(f"  [Persona]    {persona_result['label']} "
              f"(confidence: {persona_result['confidence']:.2f}, "
              f"method: {persona_result['method']})")

        
        retrieval = self.rag_pipeline.retrieve_and_format(user_message)

        print(f"  [Retrieval]  avg score: {retrieval['avg_score']:.4f}, "
              f"context found: {retrieval['has_relevant_context']}")

       
        escalation = self.escalation_engine.evaluate(
            user_message=user_message,
            retrieval_result=retrieval,
            turn_count=turn_count,
        )

       
        if escalation.should_escalate:
            self.memory.mark_escalated(session_id)
            print(f"  [Escalation] YES — {escalation.reasons}")

            
            summary = self.handoff_generator.generate(
                user_message=user_message,
                persona=persona,
                conversation_history=history,
                sources_used=retrieval["sources"],
                escalation_reasons=escalation.reasons,
                priority=escalation.priority,
                session_id=session_id,
            )

            
            if retrieval["has_relevant_context"]:
                response_text = self.response_generator.generate(
                    query=user_message,
                    persona=persona,
                    context=retrieval["context"],
                    conversation_history=history,
                )
                response_text += (
                    "\n\n---\n"
                    "I'm connecting you with a human support agent "
                    "for more specialized assistance. "
                    f"Your case has been marked as {escalation.priority} priority. "
                    "A support specialist will review your case shortly."
                )
            else:
                response_text = (
                    "I understand your concern. After reviewing our knowledge base, "
                    "I wasn't able to find a specific solution for your situation.\n\n"
                    "I'm connecting you with a human support agent "
                    "for personalized assistance. "
                    f"Your case has been marked as {escalation.priority} priority."
                )

            self.memory.add_assistant_message(
                session_id, response_text, retrieval["sources"]
            )

            return AgentResponse(
                message=response_text,
                persona=persona,
                persona_label=persona_result["label"],
                persona_confidence=persona_result["confidence"],
                sources=retrieval["sources"],
                retrieval_score=retrieval["avg_score"],
                is_escalated=True,
                escalation_summary=summary,
                session_id=session_id,
            )

        else:
            
            print(f"  [Escalation] No")

            response_text = self.response_generator.generate(
                query=user_message,
                persona=persona,
                context=retrieval["context"],
                conversation_history=history,
            )

            self.memory.add_assistant_message(
                session_id, response_text, retrieval["sources"]
            )

            return AgentResponse(
                message=response_text,
                persona=persona,
                persona_label=persona_result["label"],
                persona_confidence=persona_result["confidence"],
                sources=retrieval["sources"],
                retrieval_score=retrieval["avg_score"],
                is_escalated=False,
                escalation_summary=None,
                session_id=session_id,
            )