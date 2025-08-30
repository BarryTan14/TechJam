"""
Test script for Executive Report Storage in MongoDB
"""

import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_executive_report_manager():
    """Test Executive Report Manager functionality"""
    print("🧪 Testing Executive Report Manager")
    print("=" * 50)
    
    try:
        from agents.executive_report_manager import ExecutiveReportManager
        
        # Create manager instance
        manager = ExecutiveReportManager()
        
        # Test MongoDB connection
        if manager.collection is None:
            print("❌ MongoDB connection failed")
            return False
        
        print("✅ MongoDB connection established")
        
        # Test data
        test_report = {
            "report_id": f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "prd_name": "Test PRD for Storage",
            "generated_at": datetime.now().isoformat(),
            "executive_summary": "This is a test executive summary for storage verification.",
            "key_findings": [
                "Test finding 1: System has high compliance risk",
                "Test finding 2: Multiple states require attention",
                "Test finding 3: Executive action required"
            ],
            "risk_assessment": {
                "overall_risk": "high",
                "critical_issues": 3,
                "states_at_risk": 15
            },
            "compliance_overview": {
                "total_features": 5,
                "compliance_rate": 0.6,
                "regulations_covered": ["GDPR", "CCPA"]
            },
            "recommendations": [
                "Implement additional privacy controls",
                "Review state-specific requirements",
                "Conduct compliance audit"
            ],
            "next_steps": [
                "Schedule compliance review meeting",
                "Prepare action plan",
                "Assign responsibility for implementation"
            ]
        }
        
        test_prd_id = "test_prd_123"
        test_workflow_id = "test_workflow_456"
        
        # Test storing executive report
        print("\n📝 Testing executive report storage...")
        storage_success = manager.store_executive_report(test_report, test_prd_id, test_workflow_id)
        
        if storage_success:
            print("✅ Executive report stored successfully")
        else:
            print("❌ Failed to store executive report")
            return False
        
        # Test retrieving executive report
        print("\n🔍 Testing executive report retrieval...")
        retrieved_report = manager.get_executive_report(test_report["report_id"])
        
        if retrieved_report:
            print("✅ Executive report retrieved successfully")
            print(f"   - Report ID: {retrieved_report['report_id']}")
            print(f"   - PRD Name: {retrieved_report['prd_name']}")
            print(f"   - Stored At: {retrieved_report['stored_at']}")
        else:
            print("❌ Failed to retrieve executive report")
            return False
        
        # Test retrieving by PRD ID
        print("\n📋 Testing retrieval by PRD ID...")
        prd_reports = manager.get_executive_reports_by_prd(test_prd_id)
        
        if prd_reports:
            print(f"✅ Found {len(prd_reports)} executive reports for PRD")
            for report in prd_reports:
                print(f"   - {report['report_id']}: {report['prd_name']}")
        else:
            print("❌ No executive reports found for PRD")
            return False
        
        # Test retrieving by workflow ID
        print("\n🔄 Testing retrieval by workflow ID...")
        workflow_reports = manager.get_executive_reports_by_workflow(test_workflow_id)
        
        if workflow_reports:
            print(f"✅ Found {len(workflow_reports)} executive reports for workflow")
            for report in workflow_reports:
                print(f"   - {report['report_id']}: {report['prd_name']}")
        else:
            print("❌ No executive reports found for workflow")
            return False
        
        # Test search functionality
        print("\n🔎 Testing search functionality...")
        search_results = manager.search_executive_reports("test", limit=5)
        
        if search_results:
            print(f"✅ Found {len(search_results)} executive reports matching 'test'")
            for report in search_results:
                print(f"   - {report['report_id']}: {report['prd_name']}")
        else:
            print("⚠️ No executive reports found matching 'test'")
        
        # Test update functionality
        print("\n✏️ Testing update functionality...")
        updates = {
            "executive_summary": "Updated executive summary for testing purposes.",
            "status": "updated"
        }
        
        update_success = manager.update_executive_report(test_report["report_id"], updates)
        
        if update_success:
            print("✅ Executive report updated successfully")
            
            # Verify update
            updated_report = manager.get_executive_report(test_report["report_id"])
            if updated_report and updated_report["executive_summary"] == updates["executive_summary"]:
                print("✅ Update verified successfully")
            else:
                print("❌ Update verification failed")
                return False
        else:
            print("❌ Failed to update executive report")
            return False
        
        # Test soft delete
        print("\n🗑️ Testing soft delete functionality...")
        delete_success = manager.delete_executive_report(test_report["report_id"])
        
        if delete_success:
            print("✅ Executive report soft deleted successfully")
            
            # Verify it's not returned in active reports
            active_reports = manager.get_all_executive_reports()
            deleted_found = any(r["report_id"] == test_report["report_id"] for r in active_reports)
            
            if not deleted_found:
                print("✅ Deleted report not found in active reports")
            else:
                print("❌ Deleted report still found in active reports")
                return False
        else:
            print("❌ Failed to delete executive report")
            return False
        
        print("\n🎉 All executive report storage tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_workflow_integration():
    """Test workflow integration with executive report storage"""
    print("\n🧪 Testing Workflow Integration")
    print("=" * 50)
    
    try:
        from langgraph_workflow import ComplianceWorkflow
        
        # Create workflow instance
        workflow = ComplianceWorkflow()
        
        # Test PRD data
        test_prd_data = {
            "prd_id": f"test_prd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "prd_name": "Test PRD for Workflow Integration",
            "prd_description": "Testing executive report generation and storage in workflow",
            "prd_content": """
            This is a test PRD for verifying executive report storage in the workflow.
            
            Key Features:
            1. User Authentication - Secure login system
            2. Data Processing - Automated data analysis
            3. Reporting - Compliance reporting dashboard
            
            Technical Requirements:
            - Web-based application
            - Database integration
            - API endpoints for data access
            - Security compliance with GDPR and CCPA
            """,
            "metadata": {
                "document_type": "test",
                "analysis_date": datetime.now().isoformat(),
                "source": "test_script"
            }
        }
        
        print("🚀 Running workflow with executive report generation...")
        
        # Run workflow
        final_state = workflow.run_workflow(test_prd_data)
        
        print(f"✅ Workflow completed successfully")
        print(f"   - Workflow ID: {final_state.workflow_id}")
        print(f"   - PRD Name: {final_state.prd_name}")
        print(f"   - Total Features: {len(final_state.extracted_features)}")
        
        # Check if executive report was generated
        if final_state.executive_report:
            print(f"✅ Executive report generated")
            print(f"   - Report ID: {final_state.executive_report.get('report_id')}")
            print(f"   - Generated At: {final_state.executive_report.get('generated_at')}")
            print(f"   - Summary Length: {len(final_state.executive_report.get('executive_summary', ''))} characters")
            
            # Verify storage in MongoDB
            from agents.executive_report_manager import ExecutiveReportManager
            manager = ExecutiveReportManager()
            
            stored_report = manager.get_executive_report(final_state.executive_report["report_id"])
            
            if stored_report:
                print("✅ Executive report verified in MongoDB")
                print(f"   - MongoDB ID: {stored_report['_id']}")
                print(f"   - Stored At: {stored_report['stored_at']}")
                print(f"   - Status: {stored_report['status']}")
            else:
                print("❌ Executive report not found in MongoDB")
                return False
        else:
            print("❌ No executive report generated")
            return False
        
        print("\n🎉 Workflow integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Workflow integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Executive Report Storage Test Suite")
    print("=" * 60)
    
    success = True
    
    # Test executive report manager
    if not test_executive_report_manager():
        success = False
    
    # Test workflow integration
    if not test_workflow_integration():
        success = False
    
    if success:
        print("\n🎉 All tests passed! Executive report storage is working correctly.")
        print("\n📝 Features Verified:")
        print("   ✅ MongoDB connection and collection management")
        print("   ✅ Executive report storage and retrieval")
        print("   ✅ Search and update functionality")
        print("   ✅ Soft delete functionality")
        print("   ✅ Workflow integration")
        print("   ✅ Automatic storage during workflow execution")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
