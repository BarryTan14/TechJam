#!/usr/bin/env python3
"""
Test script to verify that the executive report includes cultural sensitivity information
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.agents.executive_report_generator import ExecutiveReportGenerator
from langgraph.langgraph_workflow import WorkflowState

def test_executive_report_with_cultural_sensitivity():
    """Test that the executive report includes cultural sensitivity information"""
    print("📊 Testing Executive Report with Cultural Sensitivity")
    print("=" * 60)
    
    # Create a mock workflow state with cultural sensitivity analysis
    mock_state = WorkflowState(
        prd_id="test_prd_001",
        prd_name="Test PRD with Cultural Sensitivity",
        prd_description="A test PRD to verify cultural sensitivity integration",
        prd_content="Test content for cultural sensitivity analysis",
        metadata={
            "document_type": "test_document",
            "analysis_date": datetime.now().isoformat(),
            "word_count": 100,
            "source": "test"
        }
    )
    
    # Add cultural sensitivity analysis to the state
    mock_state.cultural_sensitivity_analysis = {
        "overall_cultural_sensitivity": "medium",
        "overall_average_score": 0.65,
        "regional_scores": {
            "united_states": {
                "average_score": 0.65,
                "score_level": "medium",
                "total_features": 3,
                "high_sensitivity_features": 1,
                "medium_sensitivity_features": 1,
                "low_sensitivity_features": 1,
                "cultural_issues": [
                    "Privacy concerns with data collection",
                    "Accessibility improvements needed",
                    "Language inclusivity considerations"
                ],
                "recommendations": [
                    "Implement clear consent mechanisms",
                    "Add ADA compliance features",
                    "Use inclusive language throughout"
                ]
            }
        },
        "key_cultural_issues": [
            "Privacy concerns with data collection",
            "Accessibility improvements needed",
            "Language inclusivity considerations"
        ],
        "recommendations": [
            "Implement clear consent mechanisms",
            "Add ADA compliance features",
            "Use inclusive language throughout",
            "Conduct user testing with diverse populations",
            "Review feature designs for cultural inclusivity"
        ],
        "total_features_analyzed": 3,
        "regions_analyzed": 1,
        "requires_human_review": True
    }
    
    # Add other required state data
    mock_state.feature_compliance_results = []
    mock_state.critical_compliance_issues = ["Test compliance issue"]
    mock_state.summary_recommendations = ["Test recommendation"]
    mock_state.overall_risk_level = "medium"
    mock_state.overall_confidence_score = 0.75
    
    # Initialize the executive report generator
    generator = ExecutiveReportGenerator()
    
    try:
        # Generate the executive report
        print("🔄 Generating executive report...")
        report = generator.generate_executive_report(mock_state)
        
        print(f"✅ Executive report generated successfully")
        print(f"📄 Report ID: {report.report_id}")
        print(f"📄 PRD Name: {report.prd_name}")
        
        # Test key findings
        print(f"\n🔍 Key Findings ({len(report.key_findings)}):")
        cultural_findings = []
        for finding in report.key_findings:
            print(f"   • {finding}")
            if "cultural" in finding.lower() or "sensitivity" in finding.lower():
                cultural_findings.append(finding)
        
        print(f"\n🇺🇸 Cultural Sensitivity Findings ({len(cultural_findings)}):")
        for finding in cultural_findings:
            print(f"   • {finding}")
        
        # Test risk assessment
        print(f"\n⚠️ Risk Assessment:")
        print(f"   • Overall Risk Level: {report.risk_assessment.get('overall_risk_level')}")
        print(f"   • Cultural Sensitivity Risk: {report.risk_assessment.get('cultural_sensitivity_risk', {})}")
        
        cultural_risk = report.risk_assessment.get('cultural_sensitivity_risk', {})
        if cultural_risk:
            print(f"   • Cultural Sensitivity Level: {cultural_risk.get('overall_sensitivity_level')}")
            print(f"   • Cultural Sensitivity Score: {cultural_risk.get('overall_sensitivity_score')}")
            print(f"   • Requires Human Review: {cultural_risk.get('requires_human_review')}")
        
        # Test recommendations
        print(f"\n💡 Recommendations ({len(report.recommendations)}):")
        cultural_recommendations = []
        for rec in report.recommendations:
            print(f"   • {rec}")
            if "[Cultural]" in rec or "cultural" in rec.lower() or "sensitivity" in rec.lower():
                cultural_recommendations.append(rec)
        
        print(f"\n🇺🇸 Cultural Sensitivity Recommendations ({len(cultural_recommendations)}):")
        for rec in cultural_recommendations:
            print(f"   • {rec}")
        
        # Test next steps
        print(f"\n🚀 Next Steps ({len(report.next_steps)}):")
        cultural_next_steps = []
        for step in report.next_steps:
            print(f"   • {step}")
            if "cultural" in step.lower() or "sensitivity" in step.lower():
                cultural_next_steps.append(step)
        
        print(f"\n🇺🇸 Cultural Sensitivity Next Steps ({len(cultural_next_steps)}):")
        for step in cultural_next_steps:
            print(f"   • {step}")
        
        # Test executive summary
        print(f"\n📋 Executive Summary:")
        print(f"   Length: {len(report.executive_summary)} characters")
        print(f"   Contains 'Cultural': {'Cultural' in report.executive_summary}")
        print(f"   Contains 'Sensitivity': {'Sensitivity' in report.executive_summary}")
        print(f"   Contains 'US': {'US' in report.executive_summary}")
        
        # Display a portion of the executive summary
        summary_preview = report.executive_summary[:500] + "..." if len(report.executive_summary) > 500 else report.executive_summary
        print(f"\n📝 Executive Summary Preview:")
        print(f"   {summary_preview}")
        
        # Verify cultural sensitivity integration
        success = True
        
        # Check if cultural sensitivity findings are included
        if not cultural_findings:
            print("❌ No cultural sensitivity findings found in key findings")
            success = False
        else:
            print("✅ Cultural sensitivity findings included in key findings")
        
        # Check if cultural sensitivity risk assessment is included
        if not cultural_risk:
            print("❌ No cultural sensitivity risk assessment found")
            success = False
        else:
            print("✅ Cultural sensitivity risk assessment included")
        
        # Check if cultural sensitivity recommendations are included
        if not cultural_recommendations:
            print("❌ No cultural sensitivity recommendations found")
            success = False
        else:
            print("✅ Cultural sensitivity recommendations included")
        
        # Check if cultural sensitivity next steps are included
        if not cultural_next_steps:
            print("❌ No cultural sensitivity next steps found")
            success = False
        else:
            print("✅ Cultural sensitivity next steps included")
        
        # Check if executive summary mentions cultural sensitivity
        if not any(term in report.executive_summary for term in ['Cultural', 'Sensitivity', 'US']):
            print("❌ Executive summary does not mention cultural sensitivity")
            success = False
        else:
            print("✅ Executive summary includes cultural sensitivity information")
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_executive_report_without_cultural_sensitivity():
    """Test that the executive report handles missing cultural sensitivity gracefully"""
    print("\n📊 Testing Executive Report without Cultural Sensitivity")
    print("=" * 60)
    
    # Create a mock workflow state without cultural sensitivity analysis
    mock_state = WorkflowState(
        prd_id="test_prd_002",
        prd_name="Test PRD without Cultural Sensitivity",
        prd_description="A test PRD without cultural sensitivity analysis",
        prd_content="Test content without cultural sensitivity",
        metadata={
            "document_type": "test_document",
            "analysis_date": datetime.now().isoformat(),
            "word_count": 100,
            "source": "test"
        }
    )
    
    # Add other required state data
    mock_state.feature_compliance_results = []
    mock_state.critical_compliance_issues = ["Test compliance issue"]
    mock_state.summary_recommendations = ["Test recommendation"]
    mock_state.overall_risk_level = "low"
    mock_state.overall_confidence_score = 0.85
    
    # Initialize the executive report generator
    generator = ExecutiveReportGenerator()
    
    try:
        # Generate the executive report
        print("🔄 Generating executive report...")
        report = generator.generate_executive_report(mock_state)
        
        print(f"✅ Executive report generated successfully")
        print(f"📄 Report ID: {report.report_id}")
        
        # Check that the report handles missing cultural sensitivity gracefully
        cultural_findings = [f for f in report.key_findings if "cultural" in f.lower() or "sensitivity" in f.lower()]
        
        if cultural_findings:
            print("❌ Cultural sensitivity findings found when none should exist")
            return False
        else:
            print("✅ No cultural sensitivity findings found (as expected)")
        
        # Check that the report still generates successfully
        if not report.executive_summary:
            print("❌ Executive summary is empty")
            return False
        else:
            print("✅ Executive summary generated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Executive Report Cultural Sensitivity Integration Test Suite")
    print("=" * 60)
    
    # Test 1: Executive report with cultural sensitivity
    test1_success = test_executive_report_with_cultural_sensitivity()
    
    # Test 2: Executive report without cultural sensitivity
    test2_success = test_executive_report_without_cultural_sensitivity()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   With Cultural Sensitivity: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   Without Cultural Sensitivity: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success
    
    if overall_success:
        print("\n🎉 All tests passed! Executive report cultural sensitivity integration is working correctly.")
        print("\n📋 Key Features Verified:")
        print("   • Cultural sensitivity findings included in key findings")
        print("   • Cultural sensitivity risk assessment included")
        print("   • Cultural sensitivity recommendations included")
        print("   • Cultural sensitivity next steps included")
        print("   • Executive summary mentions cultural sensitivity")
        print("   • Graceful handling of missing cultural sensitivity data")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
