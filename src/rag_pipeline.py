"""
RAG Pipeline

Wraps the knowledge base retrieval and formats the output
for the response generator.
"""

from .config import config
from .knowledge_base import KnowledgeBase


class RAGPipeline:
    """Orchestrates retrieval and context formatting."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base

    def retrieve_and_format(self, query: str, k: int = None) -> dict:
        """
        Retrieve relevant documents and format for response generation.

        Returns:
            {
                "context": str,
                "sources": list,
                "avg_score": float,
                "min_score": float,
                "has_relevant_context": bool,
            }
        """
        results = self.kb.retrieve(query, k=k)

        if not results:
            return {
                "context": "",
                "sources": [],
                "avg_score": 0.0,
                "min_score": 0.0,
                "has_relevant_context": False,
            }

        scores = [r["score"] for r in results]
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)

        # Format context for the LLM
        context_parts = []
        sources = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {i}: {result['source']} - {result['section']}]\n"
                f"{result['content']}"
            )
            sources.append({
                "source": result["source"],
                "section": result["section"],
                "page": result.get("page"),
                "relevance_score": round(result["score"], 4),
            })

        context = "\n\n---\n\n".join(context_parts)

        return {
            "context": context,
            "sources": sources,
            "avg_score": round(avg_score, 4),
            "min_score": round(min_score, 4),
            "has_relevant_context": avg_score >= config.SIMILARITY_THRESHOLD,
        }