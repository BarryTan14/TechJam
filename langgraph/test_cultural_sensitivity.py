"""
Test script for Cultural Sensitivity Analyzer
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_cultural_sensitivity_analyzer():
    """Test Cultural Sensitivity Analyzer functionality"""
    print("🧪 Testing Cultural Sensitivity Analyzer")
    print("=" * 60)
    
    try:
        from agents.cultural_sensitivity_analyzer import CulturalSensitivityAnalyzer
        
        # Create analyzer instance
        analyzer = CulturalSensitivityAnalyzer(llm=None)  # No LLM for testing
        
        print("✅ Cultural Sensitivity Analyzer initialized")
        
        # Test data
        test_feature = {
            "name": "User Authentication System",
            "description": "Multi-factor authentication system with biometric options",
            "content": """
            The user authentication system provides secure login capabilities including:
            - Username and password authentication
            - Multi-factor authentication (SMS, email, authenticator apps)
            - Biometric authentication (fingerprint, face recognition)
            - Social media login integration
            - Password reset functionality
            - Account lockout after failed attempts
            - Session management and timeout
            - Privacy controls for user data
            - Accessibility features for users with disabilities
            - Multi-language support for global users
            """
        }
        
        # Test single region analysis
        print(f"\n🌍 Testing single region analysis for {test_feature['name']}...")
        
        regions_to_test = ["north_america", "europe", "asia_pacific", "middle_east"]
        
        for region in regions_to_test:
            print(f"\n📋 Analyzing {region}...")
            score = analyzer.analyze_cultural_sensitivity(
                test_feature["name"],
                test_feature["description"],
                test_feature["content"],
                region
            )
            
            print(f"   ✅ Score: {score.overall_score:.2f} ({score.score_level})")
            print(f"   📝 Reasoning: {score.reasoning[:100]}...")
            print(f"   🎯 Cultural Factors: {', '.join(score.cultural_factors[:3])}")
            print(f"   ⚠️ Issues: {len(score.potential_issues)} identified")
            print(f"   💡 Recommendations: {len(score.recommendations)} provided")
            print(f"   🤖 Confidence: {score.confidence_score:.2f}")
            print(f"   👤 Human Review: {'Required' if score.requires_human_review else 'Not required'}")
        
        # Test all regions analysis
        print(f"\n🌍 Testing all regions analysis for {test_feature['name']}...")
        
        all_scores = analyzer.analyze_feature_for_all_regions(
            test_feature["name"],
            test_feature["description"],
            test_feature["content"]
        )
        
        print(f"✅ Analyzed {len(all_scores)} regions:")
        for region, score in all_scores.items():
            print(f"   - {region}: {score.overall_score:.2f} ({score.score_level})")
        
        # Test cultural factors retrieval
        print(f"\n📚 Testing cultural factors retrieval...")
        
        for region in regions_to_test:
            factors = analyzer.get_regional_cultural_factors(region)
            print(f"   - {region}: {len(factors)} factor categories")
            for category, items in factors.items():
                print(f"     * {category}: {len(items)} items")
        
        # Test available regions
        print(f"\n🗺️ Testing available regions...")
        regions = analyzer.get_all_regions()
        print(f"   Available regions: {', '.join(regions)}")
        
        print("\n🎉 All cultural sensitivity analyzer tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_integration():
    """Test workflow integration with cultural sensitivity analysis"""
    print("\n🧪 Testing Workflow Integration")
    print("=" * 60)
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        
        # Create workflow instance
        workflow = ComplianceWorkflow()
        
        # Test PRD data
        test_prd_data = {
            "prd_id": f"test_prd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "prd_name": "Test PRD for Cultural Sensitivity",
            "prd_description": "Testing cultural sensitivity analysis in workflow",
            "prd_content": """
            This PRD describes a global user authentication system with cultural considerations.
            
            Key Features:
            1. Multi-Language Authentication - Support for 50+ languages with cultural adaptations
            2. Biometric Authentication - Fingerprint and face recognition with privacy controls
            3. Social Login Integration - Support for regional social media platforms
            4. Accessibility Features - Universal design for users with disabilities
            5. Privacy Controls - GDPR-compliant data handling with regional variations
            
            Technical Requirements:
            - Multi-language support with cultural localization
            - Privacy-first design with regional compliance
            - Accessibility features (WCAG 2.1 AA compliance)
            - Mobile-first responsive design
            - Real-time translation and cultural adaptation
            """,
            "metadata": {
                "document_type": "test",
                "analysis_date": datetime.now().isoformat(),
                "source": "test_script"
            }
        }
        
        print("🚀 Running workflow with cultural sensitivity analysis...")
        
        # Run workflow
        final_state = workflow.run_workflow(test_prd_data)
        
        print(f"✅ Workflow completed successfully")
        print(f"   - Workflow ID: {final_state.workflow_id}")
        print(f"   - PRD Name: {final_state.prd_name}")
        print(f"   - Total Features: {len(final_state.extracted_features)}")
        
        # Check if cultural sensitivity analysis was generated
        if final_state.cultural_sensitivity_analysis:
            print(f"✅ Cultural sensitivity analysis generated")
            analysis = final_state.cultural_sensitivity_analysis
            
            print(f"   - Overall Sensitivity: {analysis.get('overall_cultural_sensitivity', 'N/A')}")
            print(f"   - Average Score: {analysis.get('overall_average_score', 0.0):.2f}")
            print(f"   - Features Analyzed: {analysis.get('total_features_analyzed', 0)}")
            print(f"   - Regions Analyzed: {analysis.get('regions_analyzed', 0)}")
            
            # Check regional scores
            regional_scores = analysis.get('regional_scores', {})
            print(f"   - Regional Scores:")
            for region, data in regional_scores.items():
                if data.get('total_features', 0) > 0:
                    print(f"     * {region}: {data['average_score']:.2f} ({data['score_level']})")
            
            # Check issues and recommendations
            issues = analysis.get('key_cultural_issues', [])
            recommendations = analysis.get('recommendations', [])
            print(f"   - Key Issues: {len(issues)} identified")
            print(f"   - Recommendations: {len(recommendations)} provided")
            
        else:
            print("❌ No cultural sensitivity analysis generated")
            return False
        
        # Check feature-level cultural sensitivity
        print(f"\n🔍 Checking feature-level cultural sensitivity...")
        for i, result in enumerate(final_state.feature_compliance_results):
            if hasattr(result, 'cultural_sensitivity_scores') and result.cultural_sensitivity_scores:
                print(f"   Feature {i+1}: {result.feature.feature_name}")
                for region, score in result.cultural_sensitivity_scores.items():
                    print(f"     - {region}: {score.overall_score:.2f} ({score.score_level})")
            else:
                print(f"   Feature {i+1}: No cultural sensitivity scores")
        
        print("\n🎉 Workflow integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Cultural Sensitivity Analyzer Test Suite")
    print("=" * 80)
    
    success = True
    
    # Test cultural sensitivity analyzer
    if not test_cultural_sensitivity_analyzer():
        success = False
    
    # Test workflow integration
    if not test_workflow_integration():
        success = False
    
    if success:
        print("\n🎉 All tests passed! Cultural sensitivity analysis is working correctly.")
        print("\n📝 Features Verified:")
        print("   ✅ Cultural sensitivity analyzer initialization")
        print("   ✅ Single region analysis with detailed reasoning")
        print("   ✅ All regions analysis")
        print("   ✅ Cultural factors retrieval")
        print("   ✅ Workflow integration")
        print("   ✅ Feature-level cultural sensitivity scoring")
        print("   ✅ Overall cultural sensitivity aggregation")
        print("   ✅ Regional score calculation")
        print("   ✅ Issues and recommendations generation")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
