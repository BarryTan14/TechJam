#!/usr/bin/env python3
"""
Test script to verify workflow storage functionality
Tests that both executive reports and cultural sensitivity analysis are stored in MongoDB
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.langgraph_workflow import ComplianceWorkflow, WorkflowState
from langgraph.agents.executive_report_manager import ExecutiveReportManager

def test_workflow_storage():
    """Test that the workflow stores both executive reports and cultural sensitivity analysis"""
    print("🧪 Testing workflow storage functionality...")
    
    # Initialize the workflow
    workflow = ComplianceWorkflow()
    
    if not workflow.llm:
        print("❌ LLM not available, skipping test")
        return False
    
    # Create a test PRD state
    test_state = WorkflowState(
        prd_id="test_prd_001",
        prd_name="Test PRD for Storage",
        prd_description="A test PRD to verify storage functionality",
        prd_content="""
        # Test Product Requirements Document
        
        ## Feature 1: User Authentication
        The system should provide secure user authentication with multi-factor authentication support.
        
        ## Feature 2: Data Privacy Controls
        Users should be able to control their privacy settings and data sharing preferences.
        
        ## Feature 3: Payment Processing
        The system should support multiple payment methods including credit cards and digital wallets.
        
        ## Feature 4: Content Moderation
        The platform should include automated content moderation with human review capabilities.
        """,
        metadata={
            "document_type": "test_document",
            "analysis_date": datetime.now().isoformat(),
            "word_count": 50,
            "source": "test"
        }
    )
    
    print(f"📝 Created test state with PRD ID: {test_state.prd_id}")
    
    try:
        # Run the workflow
        print("🔄 Running workflow...")
        final_state = workflow.run_workflow(test_state)
        
        print(f"✅ Workflow completed successfully")
        print(f"📊 Executive report generated: {final_state.executive_report is not None}")
        print(f"🌍 Cultural sensitivity analysis generated: {final_state.cultural_sensitivity_analysis is not None}")
        
        # Test retrieval from MongoDB
        print("\n🔍 Testing MongoDB retrieval...")
        manager = ExecutiveReportManager()
        
        # Test executive report retrieval
        executive_reports = manager.get_executive_reports_by_workflow(final_state.workflow_id)
        print(f"📄 Executive reports found: {len(executive_reports)}")
        
        if executive_reports:
            report = executive_reports[0]
            print(f"   - Report ID: {report.get('report_id')}")
            print(f"   - PRD Name: {report.get('prd_name')}")
            print(f"   - Status: {report.get('status')}")
        
        # Test cultural sensitivity analysis retrieval
        cultural_analyses = manager.get_cultural_sensitivity_analyses_by_workflow(final_state.workflow_id)
        print(f"🌍 Cultural sensitivity analyses found: {len(cultural_analyses)}")
        
        if cultural_analyses:
            analysis = cultural_analyses[0]
            print(f"   - Analysis ID: {analysis.get('analysis_id')}")
            print(f"   - Overall Sensitivity: {analysis.get('overall_cultural_sensitivity')}")
            print(f"   - Average Score: {analysis.get('overall_average_score')}")
            print(f"   - Status: {analysis.get('status')}")
        
        # Test retrieval by PRD ID
        print(f"\n🔍 Testing retrieval by PRD ID: {final_state.prd_id}")
        
        prd_executive_reports = manager.get_executive_reports_by_prd(final_state.prd_id)
        print(f"📄 Executive reports for PRD: {len(prd_executive_reports)}")
        
        prd_cultural_analyses = manager.get_cultural_sensitivity_analyses_by_prd(final_state.prd_id)
        print(f"🌍 Cultural sensitivity analyses for PRD: {len(prd_cultural_analyses)}")
        
        # Verify data integrity
        success = True
        
        if not executive_reports:
            print("❌ No executive reports found in MongoDB")
            success = False
        else:
            print("✅ Executive reports stored successfully")
        
        if not cultural_analyses:
            print("❌ No cultural sensitivity analyses found in MongoDB")
            success = False
        else:
            print("✅ Cultural sensitivity analyses stored successfully")
        
        if len(prd_executive_reports) != len(executive_reports):
            print("❌ PRD-based retrieval mismatch for executive reports")
            success = False
        
        if len(prd_cultural_analyses) != len(cultural_analyses):
            print("❌ PRD-based retrieval mismatch for cultural sensitivity analyses")
            success = False
        
        return success
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_manager_functionality():
    """Test the ExecutiveReportManager functionality directly"""
    print("\n🧪 Testing ExecutiveReportManager functionality...")
    
    manager = ExecutiveReportManager()
    
    # Test data
    test_executive_report = {
        "report_id": "test_report_001",
        "prd_name": "Test PRD",
        "generated_at": datetime.now().isoformat(),
        "executive_summary": "This is a test executive summary",
        "key_findings": ["Finding 1", "Finding 2"],
        "risk_assessment": {"overall_risk": "low"},
        "compliance_overview": {"compliance_score": 0.8},
        "recommendations": ["Recommendation 1"],
        "next_steps": ["Step 1"]
    }
    
    test_cultural_analysis = {
        "overall_cultural_sensitivity": "moderate",
        "overall_average_score": 0.6,
        "regional_scores": {"North America": 0.7, "Europe": 0.5},
        "key_cultural_issues": ["Issue 1", "Issue 2"],
        "recommendations": ["Cultural recommendation 1"],
        "total_features_analyzed": 4,
        "regions_analyzed": 2,
        "requires_human_review": False
    }
    
    test_prd_id = "test_prd_manager_001"
    test_workflow_id = "test_workflow_manager_001"
    
    try:
        # Test storing both types of data
        print("💾 Testing storage of both executive report and cultural analysis...")
        success = manager.store_workflow_results(
            test_executive_report,
            test_cultural_analysis,
            test_prd_id,
            test_workflow_id
        )
        
        if not success:
            print("❌ Failed to store workflow results")
            return False
        
        print("✅ Workflow results stored successfully")
        
        # Test retrieval
        print("🔍 Testing retrieval...")
        
        # Test executive report retrieval
        reports = manager.get_executive_reports_by_workflow(test_workflow_id)
        if not reports:
            print("❌ No executive reports found")
            return False
        
        report = reports[0]
        if report.get("report_id") != test_executive_report["report_id"]:
            print("❌ Executive report ID mismatch")
            return False
        
        print("✅ Executive report retrieved successfully")
        
        # Test cultural analysis retrieval
        analyses = manager.get_cultural_sensitivity_analyses_by_workflow(test_workflow_id)
        if not analyses:
            print("❌ No cultural sensitivity analyses found")
            return False
        
        analysis = analyses[0]
        if analysis.get("overall_cultural_sensitivity") != test_cultural_analysis["overall_cultural_sensitivity"]:
            print("❌ Cultural analysis data mismatch")
            return False
        
        print("✅ Cultural sensitivity analysis retrieved successfully")
        
        # Test search functionality
        print("🔍 Testing search functionality...")
        
        search_results = manager.search_executive_reports("test")
        if not search_results:
            print("❌ Executive report search failed")
            return False
        
        cultural_search_results = manager.search_cultural_sensitivity_analyses("moderate")
        if not cultural_search_results:
            print("❌ Cultural sensitivity analysis search failed")
            return False
        
        print("✅ Search functionality working")
        
        # Clean up test data
        print("🧹 Cleaning up test data...")
        for report in reports:
            manager.delete_executive_report(report["report_id"])
        
        for analysis in analyses:
            manager.delete_cultural_sensitivity_analysis(analysis["analysis_id"])
        
        print("✅ Test data cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Manager test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Starting workflow storage tests...")
    print("=" * 50)
    
    # Test 1: Manager functionality
    manager_success = test_manager_functionality()
    
    # Test 2: Workflow integration
    workflow_success = test_workflow_storage()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Manager Functionality: {'✅ PASS' if manager_success else '❌ FAIL'}")
    print(f"   Workflow Integration: {'✅ PASS' if workflow_success else '❌ FAIL'}")
    
    overall_success = manager_success and workflow_success
    
    if overall_success:
        print("\n🎉 All tests passed! Cultural sensitivity analysis is being stored in MongoDB.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
