"""
Simple test script to verify MongoDB connection and RAG functionality
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🔌 Testing MongoDB connection...")
    
    try:
        from agents import PRDParserAgent
        
        # Create PRD Parser Agent
        agent = PRDParserAgent(llm=None)
        
        # Check if MongoDB connection is established
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
        import traceback
        traceback.print_exc()
        return False

def test_rag_functionality():
    """Test RAG functionality"""
    print("\n🔍 Testing RAG functionality...")
    
    try:
        from agents import PRDParserAgent
        
        agent = PRDParserAgent(llm=None)
        
        # Test content with terms
        test_content = """
        This PRD describes a Compliance Detection System (CDS) that uses Geo-handler (GH) 
        for routing features. The system includes Personalized feed (PF) functionality.
        """
        
        # Test term extraction
        potential_terms = agent._extract_potential_terms(test_content)
        print(f"📋 Extracted {len(potential_terms)} potential terms: {potential_terms}")
        
        # Test RAG search
        if potential_terms:
            results = agent.search_terminology(potential_terms[0], max_results=3)
            print(f"📋 Search for '{potential_terms[0]}': {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests"""
    print("🧪 Testing MongoDB Connection and RAG Functionality")
    print("=" * 60)
    
    success = True
    
    # Test MongoDB connection
    if not test_mongodb_connection():
        success = False
    
    # Test RAG functionality
    if not test_rag_functionality():
        success = False
    
    if success:
        print("\n🎉 All tests passed! MongoDB connection and RAG functionality are working.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
