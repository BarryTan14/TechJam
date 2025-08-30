import requests
import json

def test_prd_with_langgraph_integration():
    """Test PRD creation with integrated LangGraph analysis"""
    
    # Test data
    test_prd = {
        "Name": "Integrated Test Product",
        "Description": "A test product to verify LangGraph analysis integration",
        "Status": "Draft"
    }
    
    # Backend API endpoint
    url = "http://localhost:5000/api/prd"
    
    try:
        print("🧪 Testing PRD Creation with Integrated LangGraph Analysis...")
        print(f"📤 Sending request to: {url}")
        print(f"📋 Test PRD: {json.dumps(test_prd, indent=2)}")
        
        # Make the request
        response = requests.post(
            url,
            json=test_prd,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 minutes timeout
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ PRD created successfully!")
            print(f"📊 PRD ID: {result.get('ID')}")
            print(f"📋 PRD Name: {result.get('Name')}")
            
            # Check if LangGraph analysis is included
            langgraph_analysis = result.get('langgraph_analysis')
            if langgraph_analysis:
                print("✅ LangGraph analysis integrated in PRD!")
                print(f"📊 Workflow ID: {langgraph_analysis.get('workflow_id')}")
                print(f"🔴 Risk Level: {langgraph_analysis.get('overall_risk_level', 'unknown').upper()}")
                print(f"📈 Confidence: {langgraph_analysis.get('overall_confidence_score', 0):.1%}")
                print(f"⏱️ Processing Time: {langgraph_analysis.get('processing_time', 0):.2f}s")
                print(f"📋 Features Analyzed: {langgraph_analysis.get('total_features_analyzed', 0)}")
                
                # Show some recommendations
                recommendations = langgraph_analysis.get('summary_recommendations', [])
                if recommendations:
                    print(f"\n💡 Top Recommendations:")
                    for i, rec in enumerate(recommendations[:3], 1):
                        print(f"   {i}. {rec}")
                
                # Show non-compliant states
                non_compliant = langgraph_analysis.get('non_compliant_states', {})
                if non_compliant:
                    print(f"\n🇺🇸 Non-Compliant States: {len(non_compliant)}")
                    for state_code, state_data in list(non_compliant.items())[:3]:
                        print(f"   • {state_code}: {state_data.get('state_name', 'Unknown')} ({state_data.get('risk_level', 'unknown')})")
            else:
                print("⚠️ LangGraph analysis not found in PRD response.")
                print("💡 Analysis may still be running or failed.")
            
        else:
            print(f"❌ PRD creation failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Backend API. Make sure the server is running on port 5000.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The analysis is taking longer than expected.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_prd_with_langgraph_integration()
