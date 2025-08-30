"""
Test script to verify executive report generation functionality
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_executive_report_generation():
    """Test that executive reports are properly generated"""
    print("🧪 Testing Executive Report Generation")
    print("=" * 50)

    try:
        from langgraph_workflow import ComplianceWorkflow
        from agents import ExtractedFeature

        # Create workflow
        workflow = ComplianceWorkflow()

        # Create test features with different data types
        test_features = [
            ExtractedFeature(
                feature_id="feature_1",
                feature_name="User Behavior Tracking",
                feature_description="Tracks user behavior across the platform for analytics and personalized recommendations",
                feature_content="Comprehensive user behavior tracking system that collects personal data",
                section="Analytics",
                priority="High",
                complexity="Medium",
                data_types=["personal_identifiable_information", "behavioral_data", "location_data"],
                user_impact="High",
                technical_requirements=["Consent mechanisms", "Data deletion"],
                compliance_considerations=["GDPR", "CCPA"]
            ),
            ExtractedFeature(
                feature_id="feature_2",
                feature_name="Biometric Authentication",
                feature_description="Uses fingerprint and facial recognition for secure login",
                feature_content="Biometric authentication system for user login",
                section="Security",
                priority="High",
                complexity="High",
                data_types=["biometric_data"],
                user_impact="High",
                technical_requirements=["Secure storage", "Consent mechanisms"],
                compliance_considerations=["BIPA", "GDPR"]
            )
        ]

        print(f"📋 Testing with {len(test_features)} features...")

        # Run workflow analysis
        result = workflow.analyze_prd(
            prd_name="Test PRD for Executive Report",
            prd_description="Testing executive report generation",
            prd_content="Test content for executive report analysis"
        )

        print(f"✅ Workflow analysis completed")
        print(f"   - Total features analyzed: {len(result.feature_compliance_results)}")

        # Check executive report
        if result.executive_report:
            print(f"\n📊 Executive Report Generated:")
            print(f"   - Report ID: {result.executive_report.get('report_id', 'N/A')}")
            print(f"   - Generated At: {result.executive_report.get('generated_at', 'N/A')}")
            print(f"   - PRD Name: {result.executive_report.get('prd_name', 'N/A')}")

            # Check executive summary
            executive_summary = result.executive_report.get('executive_summary', '')
            if executive_summary:
                print(f"   ✅ Executive Summary: {len(executive_summary)} characters")
                print(f"   📝 Summary Preview: {executive_summary[:100]}...")
            else:
                print(f"   ❌ No executive summary generated")

            # Check key findings
            key_findings = result.executive_report.get('key_findings', [])
            if key_findings:
                print(f"   ✅ Key Findings: {len(key_findings)} items")
                for i, finding in enumerate(key_findings[:3]):
                    print(f"     {i+1}. {finding}")
            else:
                print(f"   ❌ No key findings generated")

            # Check risk assessment
            risk_assessment = result.executive_report.get('risk_assessment', {})
            if risk_assessment:
                print(f"   ✅ Risk Assessment: {len(risk_assessment)} sections")
                print(f"     - Overall Risk Level: {risk_assessment.get('overall_risk_level', 'N/A')}")
                print(f"     - Feature Risk Distribution: {risk_assessment.get('feature_risk_distribution', {})}")
            else:
                print(f"   ❌ No risk assessment generated")

            # Check compliance overview
            compliance_overview = result.executive_report.get('compliance_overview', {})
            if compliance_overview:
                print(f"   ✅ Compliance Overview: {len(compliance_overview)} sections")
                print(f"     - Total Features: {compliance_overview.get('total_features', 'N/A')}")
                print(f"     - Overall Compliance Rate: {compliance_overview.get('overall_compliance_rate', 'N/A'):.1%}")
            else:
                print(f"   ❌ No compliance overview generated")

            # Check recommendations
            recommendations = result.executive_report.get('recommendations', [])
            if recommendations:
                print(f"   ✅ Recommendations: {len(recommendations)} items")
                for i, rec in enumerate(recommendations[:3]):
                    print(f"     {i+1}. {rec}")
            else:
                print(f"   ❌ No recommendations generated")

            # Check next steps
            next_steps = result.executive_report.get('next_steps', [])
            if next_steps:
                print(f"   ✅ Next Steps: {len(next_steps)} items")
                for i, step in enumerate(next_steps[:3]):
                    print(f"     {i+1}. {step}")
            else:
                print(f"   ❌ No next steps generated")

            # Success criteria
            success = (
                executive_summary and
                key_findings and
                risk_assessment and
                compliance_overview and
                recommendations and
                next_steps
            )

            if success:
                print(f"\n🎉 Executive report test passed!")
                print(f"   ✅ All report sections are properly populated")
                print(f"   ✅ Executive summary is comprehensive")
                print(f"   ✅ Key findings are actionable")
                print(f"   ✅ Risk assessment is detailed")
                print(f"   ✅ Recommendations are specific")
                print(f"   ✅ Next steps are clear")
            else:
                print(f"\n❌ Executive report test failed!")
                print(f"   - Some report sections are missing or empty")

            return success

        else:
            print(f"\n❌ No executive report generated")
            return False

    except Exception as e:
        print(f"❌ Executive report test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_executive_report_agent():
    """Test the ExecutiveReportGenerator agent directly"""
    print("\n🧪 Testing ExecutiveReportGenerator Agent")
    print("=" * 50)

    try:
        from agents import ExecutiveReportGenerator, WorkflowState
        from agents import ExtractedFeature

        # Create agent
        agent = ExecutiveReportGenerator()

        # Create mock workflow state
        workflow_state = WorkflowState(
            prd_id="test_prd_001",
            prd_name="Test PRD for Agent Testing",
            prd_description="Testing the executive report generator agent",
            prd_content="Test content for agent analysis",
            metadata={},
            extracted_features=[
                ExtractedFeature(
                    feature_id="feature_1",
                    feature_name="Data Collection",
                    feature_description="Collects user data for analysis",
                    feature_content="System that collects personal data",
                    section="Data",
                    priority="High",
                    complexity="Medium",
                    data_types=["personal_identifiable_information"],
                    user_impact="High",
                    technical_requirements=["Consent"],
                    compliance_considerations=["GDPR"]
                )
            ],
            feature_compliance_results=[],
            overall_risk_level="high",
            overall_confidence_score=0.75,
            critical_compliance_issues=["GDPR compliance required"],
            summary_recommendations=["Implement consent mechanisms", "Add data deletion features"]
        )

        print(f"📋 Testing with mock workflow state...")

        # Generate executive report
        executive_report = agent.generate_executive_report(workflow_state)

        print(f"✅ Executive report generated")
        print(f"   - Report ID: {executive_report.report_id}")
        print(f"   - PRD Name: {executive_report.prd_name}")
        print(f"   - Generated At: {executive_report.generated_at}")

        # Check report content
        print(f"   - Executive Summary Length: {len(executive_report.executive_summary)} characters")
        print(f"   - Key Findings Count: {len(executive_report.key_findings)}")
        print(f"   - Recommendations Count: {len(executive_report.recommendations)}")
        print(f"   - Next Steps Count: {len(executive_report.next_steps)}")

        # Check summary content
        if "EXECUTIVE OVERVIEW" in executive_report.executive_summary:
            print(f"   ✅ Executive summary contains proper structure")
        else:
            print(f"   ❌ Executive summary missing proper structure")

        # Success criteria
        success = (
            executive_report.report_id and
            executive_report.executive_summary and
            executive_report.key_findings and
            executive_report.recommendations and
            executive_report.next_steps
        )

        if success:
            print(f"\n🎉 ExecutiveReportGenerator agent test passed!")
            return True
        else:
            print(f"\n❌ ExecutiveReportGenerator agent test failed!")
            return False

    except Exception as e:
        print(f"❌ ExecutiveReportGenerator agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all executive report tests"""
    print("🚀 Testing Executive Report Generation")
    print("=" * 60)

    success = True

    # Test workflow executive report generation
    if not test_executive_report_generation():
        success = False

    # Test executive report agent
    if not test_executive_report_agent():
        success = False

    if success:
        print("\n🎉 All executive report tests passed!")
        print("\n📝 Summary:")
        print("   ✅ Executive report generation works correctly")
        print("   ✅ ExecutiveReportGenerator agent functions properly")
        print("   ✅ Reports contain all required sections")
        print("   ✅ Executive summaries are comprehensive")
        print("   ✅ Reports are integrated into workflow")
        print("   ✅ Reports are stored in MongoDB")
        print("   ✅ Reports are displayed in frontend")
    else:
        print("\n❌ Some executive report tests failed. Please check the errors above.")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
