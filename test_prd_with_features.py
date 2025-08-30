import requests
import json
import time

def test_prd_with_features():
    """Test PRD creation with automatic feature creation from LangGraph analysis"""
    
    # Test data
    test_prd = {
        "Name": "Test Product with Features",
        "Description": "A test product that will trigger LangGraph analysis and feature creation",
        "Status": "Draft"
    }
    
    # Backend API endpoint
    url = "http://localhost:5000/api/prd"
    
    try:
        print("🧪 Testing PRD Creation with Automatic Feature Creation...")
        print(f"📤 Sending request to: {url}")
        print(f"📋 Test PRD: {json.dumps(test_prd, indent=2)}")
        
        # Make the request
        response = requests.post(
            url,
            json=test_prd,
            headers={"Content-Type": "application/json"},
            timeout=500  # 8+ minutes timeout for LangGraph analysis
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ PRD created successfully!")
            print(f"📊 PRD ID: {result.get('ID')}")
            print(f"📋 PRD Name: {result.get('Name')}")
            
            prd_id = result.get('ID')
            
            # Check if LangGraph analysis is included
            langgraph_analysis = result.get('langgraph_analysis')
            if langgraph_analysis:
                print("✅ LangGraph analysis integrated in PRD!")
                print(f"📊 Workflow ID: {langgraph_analysis.get('workflow_id')}")
                print(f"🔴 Risk Level: {langgraph_analysis.get('overall_risk_level', 'unknown').upper()}")
                print(f"📈 Confidence: {langgraph_analysis.get('overall_confidence_score', 0):.1%}")
                print(f"⏱️ Processing Time: {langgraph_analysis.get('processing_time', 0):.2f}s")
                print(f"📋 Features Analyzed: {langgraph_analysis.get('total_features_analyzed', 0)}")
                
                # Wait a moment for feature creation to complete
                print("\n⏳ Waiting for feature creation to complete...")
                time.sleep(5)
                
                # Get features for this PRD
                features_url = f"http://localhost:5000/api/feature-data/prd/{prd_id}"
                print(f"🔍 Checking features at: {features_url}")
                
                features_response = requests.get(features_url)
                
                if features_response.status_code == 200:
                    features = features_response.json()
                    print(f"✅ Found {len(features)} features created for PRD!")
                    
                    for i, feature in enumerate(features, 1):
                        feature_data = feature.get('data', {})
                        print(f"\n📋 Feature {i}: {feature_data.get('feature_name', 'Unknown')}")
                        print(f"   🆔 Feature ID: {feature_data.get('feature_id', 'Unknown')}")
                        print(f"   📝 Description: {feature_data.get('feature_description', 'No description')[:100]}...")
                        print(f"   🔴 Risk Level: {feature_data.get('risk_level', 'unknown').upper()}")
                        print(f"   📈 Confidence: {feature_data.get('confidence_score', 0):.1%}")
                        print(f"   🏷️ Priority: {feature_data.get('priority', 'Unknown')}")
                        print(f"   🎯 Complexity: {feature_data.get('complexity', 'Unknown')}")
                        
                        # Show compliance flags
                        compliance_flags = feature_data.get('compliance_flags', [])
                        if compliance_flags:
                            print(f"   🚩 Compliance Flags: {', '.join(compliance_flags)}")
                        
                        # Show recommendations
                        recommendations = feature_data.get('recommendations', [])
                        if recommendations:
                            print(f"   💡 Top Recommendations:")
                            for j, rec in enumerate(recommendations[:2], 1):
                                print(f"      {j}. {rec[:80]}...")
                        
                        # Show non-compliant states
                        non_compliant = feature_data.get('non_compliant_states', [])
                        if non_compliant:
                            print(f"   🇺🇸 Non-Compliant States: {len(non_compliant)} states")
                            print(f"      {', '.join(non_compliant[:5])}{'...' if len(non_compliant) > 5 else ''}")
                
                else:
                    print(f"❌ Error retrieving features: {features_response.status_code}")
                    print(f"📄 Response: {features_response.text}")
                
                # Show some recommendations
                recommendations = langgraph_analysis.get('summary_recommendations', [])
                if recommendations:
                    print(f"\n💡 Top PRD Recommendations:")
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
    test_prd_with_features()
