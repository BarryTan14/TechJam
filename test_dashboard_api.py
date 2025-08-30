import requests
import json

def test_dashboard_api():
    """Test the dashboard API endpoint that returns PRD and feature data"""
    
    # First, let's get a list of PRDs to find one with features
    try:
        print("🔍 Getting list of PRDs...")
        prds_response = requests.get("http://localhost:5000/api/prd")
        
        if prds_response.status_code == 200:
            prds = prds_response.json()
            print(f"✅ Found {len(prds)} PRDs")
            
            if len(prds) == 0:
                print("❌ No PRDs found. Please create a PRD first.")
                return
            
            # Find a PRD that has LangGraph analysis (likely has features)
            prd_with_features = None
            for prd in prds:
                if prd.get('langgraph_analysis'):
                    prd_with_features = prd
                    break
            
            if not prd_with_features:
                print("❌ No PRDs with LangGraph analysis found. Please create a PRD with analysis first.")
                return
            
            prd_id = prd_with_features['ID']
            print(f"📋 Using PRD: {prd_with_features['Name']} (ID: {prd_id})")
            
            # Test the dashboard endpoint
            dashboard_url = f"http://localhost:5000/api/prd/{prd_id}/dashboard"
            print(f"🔍 Testing dashboard endpoint: {dashboard_url}")
            
            dashboard_response = requests.get(dashboard_url)
            
            if dashboard_response.status_code == 200:
                dashboard_data = dashboard_response.json()
                print("✅ Dashboard data retrieved successfully!")
                
                # Display PRD information
                prd = dashboard_data.get('prd', {})
                print(f"\n📊 PRD Information:")
                print(f"   Name: {prd.get('Name', 'N/A')}")
                print(f"   Description: {prd.get('Description', 'N/A')}")
                print(f"   Status: {prd.get('Status', 'N/A')}")
                print(f"   Created: {prd.get('created_at', 'N/A')}")
                
                # Display feature statistics
                print(f"\n📋 Feature Statistics:")
                print(f"   Total Features: {dashboard_data.get('total_features', 0)}")
                print(f"   High Risk: {dashboard_data.get('features_with_high_risk', 0)}")
                print(f"   Medium Risk: {dashboard_data.get('features_with_medium_risk', 0)}")
                print(f"   Low Risk: {dashboard_data.get('features_with_low_risk', 0)}")
                
                # Display features
                features = dashboard_data.get('features', [])
                print(f"\n🔍 Features ({len(features)} found):")
                
                for i, feature in enumerate(features, 1):
                    feature_data = feature.get('data', {})
                    print(f"\n   Feature {i}:")
                    print(f"     UUID: {feature.get('uuid', 'N/A')}")
                    print(f"     Name: {feature_data.get('feature_name', 'N/A')}")
                    print(f"     ID: {feature_data.get('feature_id', 'N/A')}")
                    print(f"     Risk Level: {feature_data.get('risk_level', 'N/A').upper()}")
                    print(f"     Confidence: {feature_data.get('confidence_score', 0):.1%}")
                    print(f"     Priority: {feature_data.get('priority', 'N/A')}")
                    print(f"     Complexity: {feature_data.get('complexity', 'N/A')}")
                    
                    # Show compliance flags
                    compliance_flags = feature_data.get('compliance_flags', [])
                    if compliance_flags:
                        print(f"     Compliance Flags: {', '.join(compliance_flags)}")
                    
                    # Show recommendations
                    recommendations = feature_data.get('recommendations', [])
                    if recommendations:
                        print(f"     Top Recommendations:")
                        for j, rec in enumerate(recommendations[:2], 1):
                            print(f"       {j}. {rec[:80]}...")
                    
                    # Show non-compliant states
                    non_compliant = feature_data.get('non_compliant_states', [])
                    if non_compliant:
                        print(f"     Non-Compliant States: {len(non_compliant)} states")
                        print(f"       {', '.join(non_compliant[:5])}{'...' if len(non_compliant) > 5 else ''}")
                
                print(f"\n✅ Dashboard API test completed successfully!")
                
            else:
                print(f"❌ Dashboard API failed: {dashboard_response.status_code}")
                print(f"📄 Response: {dashboard_response.text}")
                
        else:
            print(f"❌ Failed to get PRDs: {prds_response.status_code}")
            print(f"📄 Response: {prds_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Backend API. Make sure the server is running on port 5000.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_dashboard_api()
