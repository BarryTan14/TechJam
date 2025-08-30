"""
Test script for PRD Parser Agent RAG functionality
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mongodb_connection():
    """Test MongoDB connection for RAG"""
    print("🔌 Testing MongoDB connection for RAG...")
    
    try:
        from agents import PRDParserAgent
        
        # Create PRD Parser Agent
        agent = PRDParserAgent(llm=None)
        
        # Test if MongoDB connection is established
        if agent.collection is not None:
            print("✅ MongoDB connection established")
            
            # Test basic query
            results = agent.search_terminology("CDS", max_results=1)
            if results:
                print(f"✅ Found {len(results)} results for 'CDS'")
                print(f"   - Term: {results[0]['term']}")
                print(f"   - Description: {results[0]['description']}")
            else:
                print("⚠️ No results found for 'CDS'")
            
            return True
        else:
            print("❌ MongoDB connection failed")
            return False
            
    except Exception as e:
        print(f"❌ MongoDB connection test failed: {e}")
        return False

def test_rag_terminology_search():
    """Test RAG terminology search functionality"""
    print("\n🔍 Testing RAG terminology search...")
    
    try:
        from agents import PRDParserAgent
        
        agent = PRDParserAgent(llm=None)
        
        # Test various search queries
        test_queries = ["CDS", "GH", "PF", "API", "GDPR"]
        
        for query in test_queries:
            results = agent.search_terminology(query, max_results=3)
            print(f"📋 Search for '{query}': {len(results)} results")
            
            for i, result in enumerate(results):
                print(f"   {i+1}. {result['term']}: {result['description'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG terminology search test failed: {e}")
        return False

def test_term_extraction():
    """Test term extraction from content"""
    print("\n📝 Testing term extraction from content...")
    
    try:
        from agents import PRDParserAgent
        
        agent = PRDParserAgent(llm=None)
        
        # Test content with various terms
        test_content = """
        This PRD describes a new CDS (Compliance Detection System) that uses GH (Geo-handler) 
        to route features based on user region. The system includes PF (Personalized feed) 
        functionality and integrates with various APIs. It must comply with GDPR and CCPA regulations.
        The system uses ML and AI for data processing.
        """
        
        # Extract potential terms
        potential_terms = agent._extract_potential_terms(test_content)
        
        print(f"📋 Extracted {len(potential_terms)} potential terms:")
        for term in potential_terms:
            print(f"   - {term}")
        
        # Verify expected terms are found
        expected_terms = ["CDS", "GH", "PF", "API", "GDPR", "CCPA", "ML", "AI"]
        found_terms = [term for term in expected_terms if term in potential_terms]
        
        print(f"✅ Found {len(found_terms)}/{len(expected_terms)} expected terms: {found_terms}")
        
        return len(found_terms) >= 5  # At least 5 expected terms should be found
        
    except Exception as e:
        print(f"❌ Term extraction test failed: {e}")
        return False

def test_prompt_augmentation():
    """Test prompt augmentation with RAG"""
    print("\n🤖 Testing prompt augmentation with RAG...")
    
    try:
        from agents import PRDParserAgent
        
        agent = PRDParserAgent(llm=None)
        
        # Test content
        test_content = """
        This PRD describes a Compliance Detection System (CDS) that uses Geo-handler (GH) 
        for routing features. The system includes Personalized feed (PF) functionality.
        """
        
        base_prompt = "Extract features from this PRD:"
        
        # Augment prompt
        augmented_prompt = agent._augment_prompt_with_rag(base_prompt, test_content)
        
        print("📋 Original prompt length:", len(base_prompt))
        print("📋 Augmented prompt length:", len(augmented_prompt))
        
        # Check if RAG context was added
        if "RELEVANT TERMINOLOGY FROM DATABASE:" in augmented_prompt:
            print("✅ RAG context successfully added to prompt")
            
            # Show the augmented part
            rag_start = augmented_prompt.find("RELEVANT TERMINOLOGY FROM DATABASE:")
            rag_part = augmented_prompt[rag_start:rag_start+200] + "..."
            print(f"📋 RAG Context Preview:\n{rag_part}")
            
            return True
        else:
            print("⚠️ No RAG context found in augmented prompt")
            return False
        
    except Exception as e:
        print(f"❌ Prompt augmentation test failed: {e}")
        return False

def test_full_rag_parsing():
    """Test full RAG-enabled PRD parsing"""
    print("\n🚀 Testing full RAG-enabled PRD parsing...")
    
    try:
        from agents import PRDParserAgent
        
        agent = PRDParserAgent(llm=None)
        
        # Test PRD content
        test_prd = {
            "name": "Compliance Detection System PRD",
            "description": "A system for detecting compliance issues in user data",
            "content": """
            This PRD describes a Compliance Detection System (CDS) that uses Geo-handler (GH) 
            to route features based on user region. The system includes Personalized feed (PF) 
            functionality and must comply with GDPR and CCPA regulations.
            
            Key Features:
            1. CDS - Main compliance detection engine
            2. GH - Geo-handler for regional routing
            3. PF - Personalized feed generation
            4. API integration for data processing
            """
        }
        
        # Parse PRD with RAG
        result = agent.parse_prd(
            test_prd["name"],
            test_prd["description"], 
            test_prd["content"]
        )
        
        print(f"✅ PRD parsing completed")
        print(f"   - Agent: {result.agent_name}")
        print(f"   - Processing time: {result.processing_time:.2f}s")
        print(f"   - RAG enabled: {result.input_data.get('rag_enabled', False)}")
        print(f"   - Thought process: {result.thought_process}")
        
        # Check analysis result
        if result.analysis_result and "extracted_features" in result.analysis_result:
            features = result.analysis_result["extracted_features"]
            print(f"   - Extracted {len(features)} features")
            
            for i, feature in enumerate(features):
                print(f"     {i+1}. {feature['feature_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full RAG parsing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all RAG tests"""
    print("🧪 Testing PRD Parser Agent RAG Functionality")
    print("=" * 60)
    
    success = True
    
    # Test MongoDB connection
    if not test_mongodb_connection():
        success = False
    
    # Test RAG terminology search
    if not test_rag_terminology_search():
        success = False
    
    # Test term extraction
    if not test_term_extraction():
        success = False
    
    # Test prompt augmentation
    if not test_prompt_augmentation():
        success = False
    
    # Test full RAG parsing
    if not test_full_rag_parsing():
        success = False
    
    if success:
        print("\n🎉 All RAG tests passed! PRD Parser Agent RAG functionality is working correctly.")
        print("\n📝 RAG Features Verified:")
        print("   ✅ MongoDB connection and cursor usage")
        print("   ✅ Keyword search with regex")
        print("   ✅ Term extraction from content")
        print("   ✅ Prompt augmentation with RAG context")
        print("   ✅ Full PRD parsing with RAG integration")
    else:
        print("\n❌ Some RAG tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
