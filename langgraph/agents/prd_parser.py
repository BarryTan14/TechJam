"""
PRD Parser Agent - Extracts features from PRD documents with RAG capabilities
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import pymongo
from pymongo import MongoClient
from pymongo.cursor import Cursor

# Import MongoDB configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mongodb_config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, CONNECTION_TIMEOUT_MS, SERVER_SELECTION_TIMEOUT_MS

from .models import AgentOutput, ExtractedFeature


class PRDParserAgent:
    """PRD Parser Agent - Extracts features from PRD documents with RAG capabilities"""
    
    def __init__(self, llm=None):
        self.llm = llm
        self.mongo_client = None
        self.collection = None
        self._initialize_mongodb()
    
    def _initialize_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            self.mongo_client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                connectTimeoutMS=CONNECTION_TIMEOUT_MS
            )
            db = self.mongo_client[DATABASE_NAME]
            self.collection = db[COLLECTION_NAME]
            # Test connection
            self.mongo_client.admin.command('ping')
            print("✅ MongoDB connection established for PRD Parser RAG")
        except Exception as e:
            print(f"⚠️ MongoDB connection failed for PRD Parser RAG: {e}")
            self.mongo_client = None
            self.collection = None
            # Ensure collection is explicitly None for proper boolean checking
            if hasattr(self, 'collection'):
                self.collection = None
    
    def _retrieve_relevant_terms(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant terms from MongoDB using RAG capabilities
        
        Args:
            query: Search query or term
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant term documents
        """
        if self.collection is None:
            return []
        
        try:
            # Create cursor for keyword search
            cursor: Cursor = self.collection.find(
                {"term": {"$regex": query, "$options": "i"}}
            ).limit(max_results)
            
            # Convert cursor to list
            results = list(cursor)
            
            # If no exact matches, try broader search
            if not results:
                # Search in descriptions as well
                cursor: Cursor = self.collection.find({
                    "$or": [
                        {"term": {"$regex": query, "$options": "i"}},
                        {"description": {"$regex": query, "$options": "i"}}
                    ]
                }).limit(max_results)
                results = list(cursor)
            
            return results
            
        except Exception as e:
            print(f"⚠️ Error retrieving terms from MongoDB: {e}")
            return []
        except AttributeError as e:
            print(f"⚠️ Collection attribute error: {e}")
            return []
    
    def _augment_prompt_with_rag(self, base_prompt: str, prd_content: str) -> str:
        """
        Augment the prompt with relevant terminology from RAG
        
        Args:
            base_prompt: Original prompt
            prd_content: PRD content to extract terms from
            
        Returns:
            Augmented prompt with RAG context
        """
        # Extract potential terms from PRD content
        potential_terms = self._extract_potential_terms(prd_content)
        
        # Retrieve relevant terms from MongoDB
        relevant_terms = []
        for term in potential_terms:
            retrieved_terms = self._retrieve_relevant_terms(term)
            relevant_terms.extend(retrieved_terms)
        
        # Remove duplicates and limit to top 3
        unique_terms = []
        seen_terms = set()
        for term_doc in relevant_terms:
            if term_doc['term'] not in seen_terms and len(unique_terms) < 3:
                unique_terms.append(term_doc)
                seen_terms.add(term_doc['term'])
        
        # If no relevant terms found, return original prompt
        if not unique_terms:
            return base_prompt + "\n\nNote: No relevant terminology found in database."
        
        # Augment prompt with RAG context
        rag_context = "\n\nRELEVANT TERMINOLOGY FROM DATABASE:\n"
        for term_doc in unique_terms:
            rag_context += f"- {term_doc['term']}: {term_doc['description']}\n"
        
        rag_context += "\nUse this terminology context to enhance your analysis and ensure consistency with established terms."
        
        return base_prompt + rag_context
    
    def _extract_potential_terms(self, content: str) -> List[str]:
        """
        Extract potential terms from PRD content for RAG lookup
        
        Args:
            content: PRD content
            
        Returns:
            List of potential terms to search for
        """
        # Common patterns for technical terms
        import re
        
        # Extract acronyms (2-4 capital letters)
        acronyms = re.findall(r'\b[A-Z]{2,4}\b', content)
        
        # Extract potential feature names (capitalized words)
        feature_names = re.findall(r'\b[A-Z][a-zA-Z]*(?:[A-Z][a-zA-Z]*)*\b', content)
        
        # Extract technical terms (words that might be terminology)
        technical_terms = re.findall(r'\b(?:API|SDK|UI|UX|DB|ML|AI|CDN|SLA|GDPR|CCPA|BIPA|HIPAA|PII|GDPR|CCPA|BIPA|HIPAA|PII|API|SDK|UI|UX|DB|ML|AI|CDN|SLA)\b', content, re.IGNORECASE)
        
        # Combine and deduplicate
        all_terms = acronyms + feature_names + technical_terms
        unique_terms = list(set(all_terms))
        
        # Filter out common words and limit to reasonable number
        common_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'MAN', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'}
        filtered_terms = [term for term in unique_terms if term.upper() not in common_words and len(term) > 1]
        
        return filtered_terms[:10]  # Limit to top 10 terms
    
    def parse_prd(self, prd_name: str, prd_description: str, prd_content: str) -> AgentOutput:
        """Parse PRD and extract features with RAG augmentation"""
        start_time = datetime.now()
        
        # Base prompt with optimized feature classification
        base_prompt = f"""You are an AI assistant that identifies and classifies "features" in software projects.

FEATURE CLASSIFICATION CRITERIA:
A **feature** is defined as a functional component or capability that:

1. **Legal/Regulatory Compliance**: Implements or enforces specific legal or regulatory requirements
   - Examples: Location-based restrictions, age gates, data retention policies, consent management
   - Must have clear legal basis (GDPR, CCPA, BIPA, HIPAA, etc.)

2. **User-Facing Functionality**: Provides user-facing functionality designed to fulfill a business or compliance need
   - Examples: Privacy controls, data export tools, consent forms, access controls
   - Must have deliberate user interaction or impact

3. **Clear Purpose and Intent**: Is deliberately rolled out or designed with a clear purpose and intention
   - Examples: Purpose-built compliance tools, regulatory enforcement mechanisms
   - Must have documented business or legal justification

CLASSIFICATION EXAMPLES:
✅ "Feature reads user location to enforce France's copyright rules (download blocking)" — Legal enforcement, qualifies as a feature
✅ "Requires age gates specific to Indonesia's Child Protection Law" — Regulatory compliance, qualifies as a feature
✅ "Data retention policy that automatically deletes user data after 30 days per GDPR requirements" — Legal compliance, qualifies as a feature
❌ "Geofences feature rollout in US for market testing" — Business/marketing driven, not a legal feature requirement
❌ "General user authentication system" — Basic functionality, not compliance-specific
❓ "A video filter feature is available globally except KR" — Ambiguous intent, requires human evaluation

EXTRACTION INSTRUCTIONS:
Analyze this PRD and extract ONLY features that meet the defined criteria:

Name: {prd_name}
Description: {prd_description}
Content: {prd_content[:2000]}{'...' if len(prd_content) > 2000 else ''}

Return JSON with this structure:
{{
    "extracted_features": [
        {{
            "feature_id": "feature_1",
            "feature_name": "Feature Name",
            "feature_description": "Brief description with legal/compliance justification",
            "feature_content": "Relevant content from PRD",
            "section": "Section name",
            "priority": "High/Medium/Low",
            "complexity": "High/Medium/Low",
            "data_types": ["data_type1"],
            "user_impact": "Impact description",
            "technical_requirements": ["req1"],
            "compliance_considerations": ["GDPR", "CCPA"],
            "legal_basis": "Specific legal regulation or requirement",
            "classification_confidence": "high/medium/low",
            "requires_human_review": false
        }}
    ],
    "total_features": 1,
    "analysis_summary": "Summary of extracted features and classification rationale",
    "classification_notes": "Notes about any ambiguous features that may need human review"
}}

IMPORTANT GUIDELINES:
- Only extract features with clear legal/compliance purpose
- If intent or legal basis is unclear, set requires_human_review to true
- Focus on compliance-specific functionality, not general business features
- Limit to 10 features maximum
- Be conservative - better to miss a feature than incorrectly classify non-features"""
        
        # Augment prompt with RAG context
        augmented_prompt = self._augment_prompt_with_rag(base_prompt, prd_content)
        
        # Execute PRD parsing using LLM with RAG
        if self.llm:
            try:
                response = self.llm.generate_content(augmented_prompt)
                
                if not response or not response.text:
                    raise Exception("LLM returned empty response")
                
                # Try to parse JSON response
                try:
                    analysis_result = json.loads(response.text)
                    thought_process = "Used LLM with RAG augmentation and feature classification to parse PRD"
                except json.JSONDecodeError:
                    analysis_result = self._extract_json_from_response(response.text)
                    thought_process = "Used LLM with RAG augmentation, feature classification, and JSON extraction"
            except Exception as e:
                print(f"⚠️ LLM parsing with RAG and feature classification failed: {e}")
                analysis_result = self._fallback_parsing_with_rag(prd_content)
                thought_process = "Used fallback parsing with RAG and feature classification due to LLM failure"
        else:
            analysis_result = self._fallback_parsing_with_rag(prd_content)
            thought_process = "Used fallback parsing with RAG and feature classification (no LLM available)"
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Create agent output
        agent_output = AgentOutput(
            agent_name="PRD Parser with RAG & Feature Classification",
            input_data={
                "prd_name": prd_name,
                "prd_description": prd_description,
                "prd_content_length": len(prd_content),
                "rag_enabled": True
            },
            thought_process=thought_process,
            analysis_result=analysis_result,
            confidence_score=0.9,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
        
        return agent_output
    
    def _fallback_parsing_with_rag(self, content: str) -> Dict[str, Any]:
        """Fallback parsing when LLM fails, with RAG context and feature classification"""
        # Get relevant terms for context
        relevant_terms = self._retrieve_relevant_terms("feature", max_results=3)
        
        rag_context = ""
        if relevant_terms:
            rag_context = "\n\nRelevant terminology found: " + ", ".join([f"{t['term']}: {t['description']}" for t in relevant_terms])
        
        return {
            "extracted_features": [
                {
                    "feature_id": "feature_1",
                    "feature_name": "PRD Feature",
                    "feature_description": f"Feature extracted from PRD content{rag_context}",
                    "feature_content": content[:500] + "..." if len(content) > 500 else content,
                    "section": "General",
                    "priority": "Medium",
                    "complexity": "Medium",
                    "data_types": ["unknown"],
                    "user_impact": "Unknown",
                    "technical_requirements": ["analysis_required"],
                    "compliance_considerations": ["GDPR", "CCPA"],
                    "legal_basis": "Requires human review - fallback parsing",
                    "classification_confidence": "low",
                    "requires_human_review": True
                }
            ],
            "total_features": 1,
            "analysis_summary": f"Created basic feature from PRD content due to parsing issues{rag_context}",
            "classification_notes": "Fallback parsing used - all features require human review for proper classification"
        }
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """Extract JSON from LLM response text"""
        import re
        
        if not response_text or not response_text.strip():
            raise Exception("LLM response is empty")
        
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove markdown code blocks
        cleaned_text = re.sub(r'^```json\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'^```\s*\n?', '', cleaned_text)
        cleaned_text = re.sub(r'\n?```\s*$', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        # Try to parse the cleaned JSON directly
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON object in the response
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, cleaned_text, re.DOTALL)
        
        if matches:
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
        
        # If no JSON found, create a basic feature with RAG and classification
        return self._fallback_parsing_with_rag(cleaned_text)
    
    def search_terminology(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search terminology database directly
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of matching term documents
        """
        return self._retrieve_relevant_terms(query, max_results)
    
    def get_all_terminology(self) -> List[Dict[str, Any]]:
        """
        Get all terminology from database
        
        Returns:
            List of all term documents
        """
        if self.collection is None:
            return []
        
        try:
            cursor: Cursor = self.collection.find({})
            return list(cursor)
        except Exception as e:
            print(f"⚠️ Error retrieving all terminology: {e}")
            return []
        except AttributeError as e:
            print(f"⚠️ Collection attribute error: {e}")
            return []
    
    def __del__(self):
        """Cleanup MongoDB connection"""
        if self.mongo_client:
            self.mongo_client.close()
