import requests
import json

def test_backend_langgraph():
    """Test the backend's LangGraph integration endpoint"""
    
    # Test data
    test_data = {
        "name": "Test Product",
        "description": "A test product for compliance analysis"
    }
    
    # Backend API endpoint
    url = "http://localhost:5000/api/langgraph/analyze"
    
    try:
        print("🧪 Testing Backend LangGraph Integration...")
        print(f"📤 Sending request to: {url}")
        print(f"📋 Test data: {json.dumps(test_data, indent=2)}")
        
        # Make the request
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minutes timeout
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend LangGraph integration successful!")
            print(f"📊 Workflow ID: {result.get('workflow_id')}")
            print(f"🔴 Risk Level: {result.get('overall_risk_level', 'unknown').upper()}")
            print(f"📈 Confidence: {result.get('overall_confidence_score', 0):.1%}")
            print(f"⏱️ Processing Time: {result.get('processing_time', 0):.2f}s")
            print(f"📋 Features Analyzed: {result.get('total_features_analyzed', 0)}")
            
            # Show some recommendations
            recommendations = result.get('summary_recommendations', [])
            if recommendations:
                print(f"\n💡 Top Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
            
            # Show non-compliant states
            non_compliant = result.get('non_compliant_states', {})
            if non_compliant:
                print(f"\n🇺🇸 Non-Compliant States: {len(non_compliant)}")
                for state_code, state_data in list(non_compliant.items())[:3]:
                    print(f"   • {state_code}: {state_data.get('state_name', 'Unknown')} ({state_data.get('risk_level', 'unknown')})")
            
        else:
            print(f"❌ Backend API call failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Backend API. Make sure the server is running on port 5000.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The analysis is taking longer than expected.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_backend_langgraph()
