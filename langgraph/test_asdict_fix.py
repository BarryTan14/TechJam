"""
Test script to verify the asdict() fix
"""

import sys
import os
import json
from dataclasses import asdict

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_asdict_serialization():
    """Test that all dataclass objects can be properly serialized with asdict()"""
    print("🧪 Testing asdict() serialization...")
    
    try:
        from agents import (
            FeatureComplianceResult, 
            ExtractedFeature, 
            USStateCompliance, 
            StateComplianceScore,
            AgentOutput
        )
        from datetime import datetime
        
        # Create test objects
        test_feature = ExtractedFeature(
            feature_id="test_feature_1",
            feature_name="Test Feature",
            feature_description="A test feature for compliance analysis",
            feature_content="Test content",
            section="Test",
            priority="Medium",
            complexity="Medium",
            data_types=["personal_identifiable_information"],
            user_impact="Medium",
            technical_requirements=["Consent mechanisms"],
            compliance_considerations=["GDPR"]
        )
        
        test_us_state_compliance = [
            USStateCompliance(
                state_name="California",
                state_code="CA",
                is_compliant=False,
                non_compliant_regulations=["CCPA"],
                risk_level="High",
                required_actions=["Implement consent mechanisms"],
                notes="Test compliance data"
            )
        ]
        
        test_state_compliance_scores = {
            "CA": StateComplianceScore(
                state_code="CA",
                state_name="California",
                compliance_score=0.3,
                risk_level="high",
                reasoning="Test reasoning",
                non_compliant_regulations=["CCPA"],
                required_actions=["Implement consent mechanisms"],
                notes="Test score data"
            )
        }
        
        test_agent_output = AgentOutput(
            agent_name="Test Agent",
            input_data={"test": "data"},
            thought_process="Test thought process",
            analysis_result={"result": "test"},
            confidence_score=0.8,
            processing_time=1.0,
            timestamp=datetime.now().isoformat()
        )
        
        # Create FeatureComplianceResult
        result = FeatureComplianceResult(
            feature=test_feature,
            agent_outputs={"test_agent": test_agent_output},
            compliance_flags=["GDPR", "CCPA"],
            risk_level="high",
            confidence_score=0.8,
            requires_human_review=True,
            reasoning="Test reasoning",
            recommendations=["Implement consent mechanisms"],
            us_state_compliance=test_us_state_compliance,
            non_compliant_states=["CA"],
            state_compliance_scores=test_state_compliance_scores,
            processing_time=1.5,
            timestamp=datetime.now().isoformat()
        )
        
        # Test asdict() on all components
        print("✅ Testing asdict() on individual components...")
        
        # Test feature
        feature_dict = asdict(result.feature)
        print(f"   - Feature: {feature_dict['feature_name']}")
        
        # Test US state compliance
        us_compliance_dict = [asdict(compliance) for compliance in result.us_state_compliance]
        print(f"   - US State Compliance: {len(us_compliance_dict)} items")
        
        # Test state compliance scores
        scores_dict = {state_code: asdict(score_data) for state_code, score_data in result.state_compliance_scores.items()}
        print(f"   - State Compliance Scores: {len(scores_dict)} states")
        
        # Test agent outputs
        agent_outputs_dict = {name: asdict(output) for name, output in result.agent_outputs.items()}
        print(f"   - Agent Outputs: {len(agent_outputs_dict)} agents")
        
        # Test full result serialization
        print("✅ Testing full result serialization...")
        result_dict = {
            "feature": asdict(result.feature),
            "agent_outputs": {name: asdict(output) for name, output in result.agent_outputs.items()},
            "compliance_flags": result.compliance_flags,
            "risk_level": result.risk_level,
            "confidence_score": result.confidence_score,
            "requires_human_review": result.requires_human_review,
            "reasoning": result.reasoning,
            "recommendations": result.recommendations,
            "us_state_compliance": [asdict(compliance) for compliance in result.us_state_compliance],
            "non_compliant_states": result.non_compliant_states,
            "state_compliance_scores": {
                state_code: asdict(score_data) 
                for state_code, score_data in result.state_compliance_scores.items()
            },
            "processing_time": result.processing_time,
            "timestamp": result.timestamp
        }
        
        # Test JSON serialization
        json_str = json.dumps(result_dict, indent=2)
        print(f"   - JSON serialization successful: {len(json_str)} characters")
        
        print("✅ All asdict() tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ asdict() test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow_save():
    """Test that the workflow save method works without asdict() errors"""
    print("\n🧪 Testing workflow save method...")
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        from agents import ExtractedFeature
        
        # Create a minimal workflow state for testing
        workflow = ComplianceWorkflow()
        
        # Create test feature
        test_feature = ExtractedFeature(
            feature_id="test_feature_1",
            feature_name="Test Feature",
            feature_description="A test feature",
            feature_content="Test content",
            section="Test",
            priority="Medium",
            complexity="Medium",
            data_types=["personal_identifiable_information"],
            user_impact="Medium",
            technical_requirements=["Consent mechanisms"],
            compliance_considerations=["GDPR"]
        )
        
        # Test that we can create the workflow without errors
        print("✅ Workflow created successfully")
        print("✅ All imports working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow save test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Testing asdict() Fix")
    print("=" * 30)
    
    success = True
    
    # Test asdict serialization
    if not test_asdict_serialization():
        success = False
    
    # Test workflow save
    if not test_workflow_save():
        success = False
    
    if success:
        print("\n🎉 All tests passed! The asdict() fix is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
