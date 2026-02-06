"""Lightweight RAG service for Vercel deployment (no ChromaDB)."""
from typing import List, Dict, Any


class RAGService:
    """Service for RAG-based retrieval of regulatory text (lightweight version)."""
    
    def __init__(self):
        """Initialize with inline regulatory data."""
        self.documents = self._get_regulatory_documents()
    
    def retrieve_relevant_rules(
        self,
        query: str,
        template_filter: str = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant regulatory text using keyword matching.
        
        Args:
            query: Natural language query
            template_filter: Optional template ID to filter by
            top_k: Number of results to return
            
        Returns:
            List of relevant documents with metadata
        """
        # Simple keyword-based retrieval for demo
        query_lower = query.lower()
        scored_docs = []
        
        for doc in self.documents:
            score = 0
            text_lower = doc["text"].lower()
            
            # Score based on keyword matches
            keywords = ["tier 1", "cet1", "own funds", "capital", "tier 2", "at1"]
            for keyword in keywords:
                if keyword in query_lower and keyword in text_lower:
                    score += 0.2
            
            # Template filter
            if template_filter and doc["metadata"].get("template") != template_filter:
                continue
                
            if score > 0:
                scored_docs.append({
                    "text": doc["text"],
                    "metadata": doc["metadata"],
                    "relevance_score": min(score, 1.0)
                })
        
        # Sort by score and return top_k
        scored_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_docs[:top_k] if scored_docs else self._get_fallback_documents()
    
    def format_context_for_llm(self, documents: List[Dict[str, Any]]) -> str:
        """Format retrieved documents for LLM prompt."""
        if not documents:
            return self._get_default_context()
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.get("metadata", {})
            source = metadata.get("source", "PRA Rulebook")
            article = metadata.get("article", "Unknown")
            
            context_parts.append(
                f"[Document {i}] {source} - {article}\n"
                f"Relevance: {doc.get('relevance_score', 0):.2f}\n"
                f"{doc['text']}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _get_regulatory_documents(self) -> List[Dict[str, Any]]:
        """Return inline regulatory documents."""
        return [
            {
                "text": """Article 25: Common Equity Tier 1 items
                
Common Equity Tier 1 (CET1) items shall comprise the following:
(a) capital instruments, provided the conditions laid down in Article 28 or, where applicable, Article 29 are met;
(b) share premium accounts related to the instruments referred to in point (a);
(c) retained earnings;
(d) accumulated other comprehensive income;
(e) other reserves;
(f) funds for general banking risk.

The items referred to in points (c) to (f) shall be recognised for the purposes of CET1 items only where they are available to the institution for unrestricted and immediate use to cover risks or losses as soon as these occur.""",
                "metadata": {
                    "source": "PRA Rulebook",
                    "article": "Article 25",
                    "template": "C_01_00",
                    "topic": "CET1 definition"
                }
            },
            {
                "text": """Article 51: Tier 1 capital
                
Tier 1 capital shall consist of the sum of Common Equity Tier 1 capital and Additional Tier 1 capital.

Common Equity Tier 1 capital shall be calculated as the sum of all the following items:
(a) CET1 items as specified in Article 25;
(b) minus the items to be deducted from CET1 items as specified in Articles 32 to 35.

Additional Tier 1 capital shall be calculated as the sum of all the following items:
(a) AT1 items as specified in Article 52;
(b) minus the items to be deducted from AT1 items as specified in Articles 52 to 56.""",
                "metadata": {
                    "source": "PRA Rulebook",
                    "article": "Article 51",
                    "template": "C_01_00",
                    "topic": "Tier 1 composition"
                }
            },
            {
                "text": """Article 72: Own funds
                
Own funds shall consist of the sum of Tier 1 capital and Tier 2 capital.

Tier 1 capital shall consist of Common Equity Tier 1 capital and Additional Tier 1 capital.

Tier 2 capital shall consist of the items specified in Article 62, minus the items to be deducted from Tier 2 capital as specified in Articles 63 to 66.

The amount of Tier 2 capital included in own funds shall not exceed one third of Tier 1 capital.""",
                "metadata": {
                    "source": "PRA Rulebook",
                    "article": "Article 72",
                    "template": "C_01_00",
                    "topic": "Own funds composition"
                }
            },
            {
                "text": """COREP Template C 01.00 - Own Funds: Instructions

Row 010 - Total own funds: This row shall contain the total amount of own funds calculated as the sum of Tier 1 capital (row 020) and Tier 2 capital (row 060).

Row 020 - Tier 1 capital: This row shall contain the total amount of Tier 1 capital calculated as the sum of Common Equity Tier 1 capital (row 030) and Additional Tier 1 capital (row 040).

Row 030 - Common Equity Tier 1 capital: This row shall contain the total amount of Common Equity Tier 1 capital after regulatory adjustments.

Row 040 - Additional Tier 1 capital: This row shall contain the total amount of Additional Tier 1 capital after regulatory adjustments.

Row 060 - Tier 2 capital: This row shall contain the total amount of Tier 2 capital after regulatory adjustments.

All amounts shall be reported in thousands of the reporting currency.""",
                "metadata": {
                    "source": "COREP Instructions",
                    "article": "Template C 01.00",
                    "template": "C_01_00",
                    "topic": "Template instructions"
                }
            }
        ]
    
    def _get_fallback_documents(self) -> List[Dict[str, Any]]:
        """Return fallback documents if retrieval fails."""
        return [{
            "text": "Article 25: Common Equity Tier 1 items comprise capital instruments, share premium, retained earnings, and other reserves.",
            "metadata": {"source": "PRA Rulebook", "article": "Article 25"},
            "relevance_score": 0.7
        }]
    
    def _get_default_context(self) -> str:
        """Return default context if no documents retrieved."""
        return """PRA Rulebook - Article 25: Common Equity Tier 1 items
        
Common Equity Tier 1 (CET1) comprises:
- Capital instruments (ordinary shares)
- Share premium
- Retained earnings
- Other reserves

Article 51: Tier 1 capital = Common Equity Tier 1 + Additional Tier 1

Article 72: Own funds = Tier 1 capital + Tier 2 capital"""
