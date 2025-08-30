#!/usr/bin/env python3
"""
Test script to verify that the FeatureComplianceResult initialization error is fixed
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import():
    """Test that the workflow can be imported without errors"""
    try:
        from langgraph.langgraph_workflow import ComplianceWorkflow
        print("✅ Successfully imported ComplianceWorkflow")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_feature_compliance_result():
    """Test that FeatureComplianceResult can be created with all required fields"""
    try:
        from langgraph.agents.models import FeatureComplianceResult, ExtractedFeature, CulturalSensitivityScore
        
        # Create a test feature
        test_feature = ExtractedFeature(
            feature_id="test_001",
            feature_name="Test Feature",
            feature_description="A test feature",
            feature_content="Test content",
            section="Test Section",
            priority="Medium",
            complexity="Medium",
            data_types=["string"],
            user_impact="Low",
            technical_requirements=["req1"],
            compliance_considerations=["comp1"]
        )
        
        # Create test cultural sensitivity scores
        test_cultural_scores = {
            "global": CulturalSensitivityScore(
                region="global",
                overall_score=0.5,
                score_level="medium",
                reasoning="Test reasoning",
                cultural_factors=["factor1"],
                potential_issues=["issue1"],
                recommendations=["rec1"],
                confidence_score=0.8,
                requires_human_review=False
            )
        }
        
        # Create FeatureComplianceResult with all required fields
        result = FeatureComplianceResult(
            feature=test_feature,
            agent_outputs={},
            compliance_flags=[],
            risk_level="low",
            confidence_score=0.8,
            requires_human_review=False,
            reasoning="Test reasoning",
            recommendations=["rec1"],
            us_state_compliance=[],
            non_compliant_states=[],
            state_compliance_scores={},
            cultural_sensitivity_scores=test_cultural_scores,
            processing_time=1.0,
            timestamp="2024-01-01T00:00:00"
        )
        
        print("✅ Successfully created FeatureComplianceResult with all required fields")
        print(f"   - Feature: {result.feature.feature_name}")
        print(f"   - Cultural sensitivity scores: {len(result.cultural_sensitivity_scores)} regions")
        return True
        
    except Exception as e:
        print(f"❌ FeatureComplianceResult creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing FeatureComplianceResult fix...")
    print("=" * 50)
    
    # Test 1: Import
    import_success = test_import()
    
    # Test 2: FeatureComplianceResult creation
    creation_success = test_feature_compliance_result()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Import Test: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"   Creation Test: {'✅ PASS' if creation_success else '❌ FAIL'}")
    
    overall_success = import_success and creation_success
    
    if overall_success:
        print("\n🎉 All tests passed! The FeatureComplianceResult initialization error is fixed.")
    else:
        print("\n⚠️ Some tests failed. The error may still exist.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
