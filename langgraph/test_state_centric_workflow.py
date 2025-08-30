#!/usr/bin/env python3
"""
Test script for the new state-centric LangGraph workflow

This script demonstrates the new approach where:
- Each state is analyzed against all features
- Results are organized by state with feature arrays
- Each feature includes risk score and reasoning
"""

import requests
import json
import time
from datetime import datetime

def test_state_centric_workflow():
    """Test the new state-centric workflow"""
    
    # Test PRD data
    prd_data = {
        "name": "E-Commerce Platform with User Analytics",
        "description": "A comprehensive e-commerce platform with user analytics, personalization, and payment processing features",
        "content": """
        Product Requirements Document: E-Commerce Platform with User Analytics
        
        Overview:
        This platform provides a complete e-commerce solution with advanced analytics and personalization capabilities.
        
        Key Features:
        1. User Authentication and Profile Management
        2. Product Catalog and Search
        3. Shopping Cart and Checkout
        4. Payment Processing
        5. Order Management
        6. User Analytics and Tracking
        7. Personalized Recommendations
        8. Email Marketing Integration
        9. Inventory Management
        10. Customer Support System
        
        Data Types:
        - Personal information (name, email, address)
        - Payment information (credit cards, billing)
        - User behavior data (browsing, purchases)
        - Analytics data (page views, conversions)
        - Marketing data (email preferences, campaigns)
        """
    }
    
    print("🚀 Testing State-Centric LangGraph Workflow")
    print("=" * 60)
    print(f"📋 PRD: {prd_data['name']}")
    print(f"📝 Description: {prd_data['description']}")
    print()
    
    # API endpoint
    url = "http://localhost:8001/analyze-prd"
    
    try:
        print("🔄 Sending request to LangGraph API...")
        start_time = time.time()
        
        response = requests.post(url, json=prd_data, timeout=None)  # No timeout
        
        end_time = time.time()
        request_time = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Analysis completed in {request_time:.2f} seconds")
            print(f"🆔 Workflow ID: {result['workflow_id']}")
            print(f"📊 Overall Risk Level: {result['overall_risk_level']}")
            print(f"🎯 Confidence Score: {result['overall_confidence_score']:.2f}")
            print(f"📈 Features Analyzed: {result['total_features_analyzed']}")
            print()
            
            # Display state-centric results
            print("🇺🇸 STATE-CENTRIC ANALYSIS RESULTS")
            print("=" * 60)
            
            state_results = result.get('state_analysis_results', {})
            
            if state_results:
                print(f"📊 Analyzed {len(state_results)} states")
                print()
                
                # Show high-risk states first
                high_risk_states = []
                medium_risk_states = []
                low_risk_states = []
                
                for state_code, state_data in state_results.items():
                    risk_level = state_data.get('overall_risk_level', 'low')
                    if risk_level == 'high':
                        high_risk_states.append((state_code, state_data))
                    elif risk_level == 'medium':
                        medium_risk_states.append((state_code, state_data))
                    else:
                        low_risk_states.append((state_code, state_data))
                
                # Display high-risk states
                if high_risk_states:
                    print("🔴 HIGH RISK STATES:")
                    for state_code, state_data in high_risk_states:
                        print(f"  {state_code} ({state_data['state_name']}):")
                        print(f"    Risk Score: {state_data['overall_risk_score']:.2f}")
                        print(f"    Non-compliant Features: {state_data['non_compliant_features']}/{state_data['total_features']}")
                        print(f"    Compliance Rate: {state_data['compliance_rate']:.1%}")
                        print()
                
                # Display medium-risk states
                if medium_risk_states:
                    print("🟡 MEDIUM RISK STATES:")
                    for state_code, state_data in medium_risk_states[:5]:  # Show first 5
                        print(f"  {state_code} ({state_data['state_name']}): {state_data['non_compliant_features']} non-compliant features")
                    if len(medium_risk_states) > 5:
                        print(f"  ... and {len(medium_risk_states) - 5} more")
                    print()
                
                # Display low-risk states summary
                if low_risk_states:
                    print(f"🟢 LOW RISK STATES: {len(low_risk_states)} states with minimal compliance issues")
                    print()
                
                # Show detailed feature analysis for a high-risk state
                if high_risk_states:
                    sample_state_code, sample_state_data = high_risk_states[0]
                    print(f"📋 DETAILED ANALYSIS FOR {sample_state_code} ({sample_state_data['state_name']}):")
                    print("-" * 50)
                    
                    features = sample_state_data.get('features', [])
                    for i, feature_data in enumerate(features[:3], 1):  # Show first 3 features
                        feature = feature_data.get('feature', {})
                        print(f"  {i}. {feature.get('feature_name', 'Unknown Feature')}")
                        print(f"     Risk Level: {feature_data.get('risk_level', 'unknown')}")
                        print(f"     Risk Score: {feature_data.get('risk_score', 0):.2f}")
                        print(f"     Compliant: {'✅' if feature_data.get('is_compliant') else '❌'}")
                        print(f"     Reasoning: {feature_data.get('reasoning', 'No reasoning provided')[:100]}...")
                        print()
                
                # Save results to file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"state_centric_results_{timestamp}.json"
                
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                
                print(f"💾 Results saved to: {filename}")
                
            else:
                print("⚠️ No state analysis results found in response")
                
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - this is expected for long-running analysis")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - make sure the LangGraph server is running on port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_state_centric_workflow()
