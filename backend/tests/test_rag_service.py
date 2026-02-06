"""Tests for RAG service."""
import pytest
from app.services.rag_service import RAGService

class TestRAGService:
    """Test suite for RAGService."""
    
    def test_initialization(self):
        """Test that RAG service initializes correctly."""
        service = RAGService()
        assert service.collection is not None
        assert service.client is not None
    
    def test_retrieve_relevant_rules(self):
        """Test retrieval of relevant regulatory text."""
        service = RAGService()
        
        query = "What is Common Equity Tier 1?"
        documents = service.retrieve_relevant_rules(query, top_k=3)
        
        assert len(documents) > 0
        assert len(documents) <= 3
        assert all("text" in doc for doc in documents)
        assert all("metadata" in doc for doc in documents)
        assert all("relevance_score" in doc for doc in documents)
    
    def test_retrieve_with_template_filter(self):
        """Test retrieval with template filtering."""
        service = RAGService()
        
        query = "Tier 1 capital composition"
        documents = service.retrieve_relevant_rules(
            query, 
            template_filter="C_01_00",
            top_k=5
        )
        
        assert len(documents) > 0
        # All documents should be related to C_01_00 template
        assert all(
            doc.get("metadata", {}).get("template") == "C_01_00" 
            for doc in documents 
            if "template" in doc.get("metadata", {})
        )
    
    def test_relevance_scores(self):
        """Test that relevance scores are between 0 and 1."""
        service = RAGService()
        
        query = "How to calculate own funds?"
        documents = service.retrieve_relevant_rules(query)
        
        for doc in documents:
            score = doc.get("relevance_score", 0)
            assert 0 <= score <= 1, f"Relevance score {score} out of range"
    
    def test_format_context_for_llm(self):
        """Test formatting of retrieved documents for LLM."""
        service = RAGService()
        
        documents = [
            {
                "text": "Article 25: CET1 comprises ordinary shares...",
                "metadata": {"source": "PRA Rulebook", "article": "Article 25"},
                "relevance_score": 0.95
            },
            {
                "text": "Article 51: Tier 1 = CET1 + AT1",
                "metadata": {"source": "PRA Rulebook", "article": "Article 51"},
                "relevance_score": 0.88
            }
        ]
        
        context = service.format_context_for_llm(documents)
        
        assert isinstance(context, str)
        assert len(context) > 0
        assert "Article 25" in context
        assert "Article 51" in context
        assert "0.95" in context or "95" in context  # Relevance score
    
    def test_empty_query_handling(self):
        """Test handling of empty queries."""
        service = RAGService()
        
        documents = service.retrieve_relevant_rules("", top_k=3)
        
        # Should still return documents (fallback behavior)
        assert isinstance(documents, list)
    
    def test_fallback_documents(self):
        """Test fallback mechanism when retrieval fails."""
        service = RAGService()
        
        fallback = service._get_fallback_documents()
        
        assert len(fallback) > 0
        assert all("text" in doc for doc in fallback)
        assert all("metadata" in doc for doc in fallback)
    
    def test_default_context(self):
        """Test default context generation."""
        service = RAGService()
        
        context = service._get_default_context()
        
        assert isinstance(context, str)
        assert len(context) > 0
        assert "Article" in context
