"""
Executive Report Manager Agent
Manages executive reports and cultural sensitivity analysis in MongoDB database
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import pymongo
from pymongo import MongoClient
from pymongo.cursor import Cursor

# Import MongoDB configuration
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mongodb_config import MONGO_URI, DATABASE_NAME, EXECUTIVE_REPORTS_COLLECTION, CULTURAL_SENSITIVITY_COLLECTION, CONNECTION_TIMEOUT_MS, SERVER_SELECTION_TIMEOUT_MS


class ExecutiveReportManager:
    """Agent for managing executive reports and cultural sensitivity analysis in MongoDB"""
    
    def __init__(self):
        self.mongo_client = None
        self.executive_reports_collection = None
        self.cultural_sensitivity_collection = None
        self._initialize_mongodb()
    
    def _initialize_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            self.mongo_client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
                connectTimeoutMS=CONNECTION_TIMEOUT_MS
            )
            db = self.mongo_client[DATABASE_NAME]
            self.executive_reports_collection = db[EXECUTIVE_REPORTS_COLLECTION]
            self.cultural_sensitivity_collection = db[CULTURAL_SENSITIVITY_COLLECTION]
            # Test connection
            self.mongo_client.admin.command('ping')
            print("✅ MongoDB connection established for Executive Report Manager")
        except Exception as e:
            print(f"⚠️ MongoDB connection failed for Executive Report Manager: {e}")
            self.mongo_client = None
            self.executive_reports_collection = None
            self.cultural_sensitivity_collection = None
    
    def store_executive_report(self, executive_report: Dict[str, Any], prd_id: str, workflow_id: str) -> bool:
        """
        Store executive report in MongoDB
        
        Args:
            executive_report: Executive report data
            prd_id: PRD identifier
            workflow_id: Workflow identifier
            
        Returns:
            True if successful, False otherwise
        """
        if self.executive_reports_collection is None:
            print("❌ MongoDB connection not available")
            return False
        
        try:
            # Prepare document for storage
            document = {
                "report_id": executive_report.get("report_id"),
                "prd_id": prd_id,
                "workflow_id": workflow_id,
                "prd_name": executive_report.get("prd_name"),
                "generated_at": executive_report.get("generated_at"),
                "executive_summary": executive_report.get("executive_summary"),
                "key_findings": executive_report.get("key_findings", []),
                "risk_assessment": executive_report.get("risk_assessment", {}),
                "compliance_overview": executive_report.get("compliance_overview", {}),
                "recommendations": executive_report.get("recommendations", []),
                "next_steps": executive_report.get("next_steps", []),
                "stored_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            # Insert document
            result = self.executive_reports_collection.insert_one(document)
            
            if result.inserted_id:
                print(f"✅ Executive report stored successfully: {result.inserted_id}")
                return True
            else:
                print("❌ Failed to store executive report")
                return False
                
        except Exception as e:
            print(f"❌ Error storing executive report: {e}")
            return False
    
    def store_cultural_sensitivity_analysis(self, cultural_analysis: Dict[str, Any], prd_id: str, workflow_id: str) -> bool:
        """
        Store cultural sensitivity analysis in MongoDB
        
        Args:
            cultural_analysis: Cultural sensitivity analysis data
            prd_id: PRD identifier
            workflow_id: Workflow identifier
            
        Returns:
            True if successful, False otherwise
        """
        if self.cultural_sensitivity_collection is None:
            print("❌ MongoDB connection not available")
            return False
        
        try:
            # Prepare document for storage
            document = {
                "analysis_id": f"cultural_{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "prd_id": prd_id,
                "workflow_id": workflow_id,
                "overall_cultural_sensitivity": cultural_analysis.get("overall_cultural_sensitivity", "unknown"),
                "overall_average_score": cultural_analysis.get("overall_average_score", 0.0),
                "regional_scores": cultural_analysis.get("regional_scores", {}),
                "key_cultural_issues": cultural_analysis.get("key_cultural_issues", []),
                "recommendations": cultural_analysis.get("recommendations", []),
                "total_features_analyzed": cultural_analysis.get("total_features_analyzed", 0),
                "regions_analyzed": cultural_analysis.get("regions_analyzed", 0),
                "requires_human_review": cultural_analysis.get("requires_human_review", True),
                "stored_at": datetime.now().isoformat(),
                "status": "active"
            }
            
            # Insert document
            result = self.cultural_sensitivity_collection.insert_one(document)
            
            if result.inserted_id:
                print(f"✅ Cultural sensitivity analysis stored successfully: {result.inserted_id}")
                return True
            else:
                print("❌ Failed to store cultural sensitivity analysis")
                return False
                
        except Exception as e:
            print(f"❌ Error storing cultural sensitivity analysis: {e}")
            return False
    
    def store_workflow_results(self, executive_report: Dict[str, Any], cultural_analysis: Dict[str, Any], prd_id: str, workflow_id: str) -> bool:
        """
        Store both executive report and cultural sensitivity analysis in MongoDB
        
        Args:
            executive_report: Executive report data
            cultural_analysis: Cultural sensitivity analysis data
            prd_id: PRD identifier
            workflow_id: Workflow identifier
            
        Returns:
            True if both stored successfully, False otherwise
        """
        executive_success = self.store_executive_report(executive_report, prd_id, workflow_id)
        cultural_success = self.store_cultural_sensitivity_analysis(cultural_analysis, prd_id, workflow_id)
        
        return executive_success and cultural_success
    
    def get_executive_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve executive report by report ID
        
        Args:
            report_id: Report identifier
            
        Returns:
            Executive report document or None
        """
        if self.executive_reports_collection is None:
            return None
        
        try:
            document = self.executive_reports_collection.find_one({"report_id": report_id})
            return document
        except Exception as e:
            print(f"❌ Error retrieving executive report: {e}")
            return None
    
    def get_cultural_sensitivity_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cultural sensitivity analysis by analysis ID
        
        Args:
            analysis_id: Analysis identifier
            
        Returns:
            Cultural sensitivity analysis document or None
        """
        if self.cultural_sensitivity_collection is None:
            return None
        
        try:
            document = self.cultural_sensitivity_collection.find_one({"analysis_id": analysis_id})
            return document
        except Exception as e:
            print(f"❌ Error retrieving cultural sensitivity analysis: {e}")
            return None
    
    def get_executive_reports_by_prd(self, prd_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all executive reports for a PRD
        
        Args:
            prd_id: PRD identifier
            
        Returns:
            List of executive report documents
        """
        if self.executive_reports_collection is None:
            return []
        
        try:
            cursor: Cursor = self.executive_reports_collection.find({"prd_id": prd_id}).sort("generated_at", -1)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error retrieving executive reports for PRD: {e}")
            return []
    
    def get_cultural_sensitivity_analyses_by_prd(self, prd_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all cultural sensitivity analyses for a PRD
        
        Args:
            prd_id: PRD identifier
            
        Returns:
            List of cultural sensitivity analysis documents
        """
        if self.cultural_sensitivity_collection is None:
            return []
        
        try:
            cursor: Cursor = self.cultural_sensitivity_collection.find({"prd_id": prd_id}).sort("stored_at", -1)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error retrieving cultural sensitivity analyses for PRD: {e}")
            return []
    
    def get_executive_reports_by_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve executive report by workflow ID
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            List of executive report documents
        """
        if self.executive_reports_collection is None:
            return []
        
        try:
            cursor: Cursor = self.executive_reports_collection.find({"workflow_id": workflow_id})
            return list(cursor)
        except Exception as e:
            print(f"❌ Error retrieving executive report for workflow: {e}")
            return []
    
    def get_cultural_sensitivity_analyses_by_workflow(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve cultural sensitivity analysis by workflow ID
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            List of cultural sensitivity analysis documents
        """
        if self.cultural_sensitivity_collection is None:
            return []
        
        try:
            cursor: Cursor = self.cultural_sensitivity_collection.find({"workflow_id": workflow_id})
            return list(cursor)
        except Exception as e:
            print(f"❌ Error retrieving cultural sensitivity analysis for workflow: {e}")
            return []
    
    def update_executive_report(self, report_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update executive report
        
        Args:
            report_id: Report identifier
            updates: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        if self.executive_reports_collection is None:
            return False
        
        try:
            updates["updated_at"] = datetime.now().isoformat()
            result = self.executive_reports_collection.update_one(
                {"report_id": report_id},
                {"$set": updates}
            )
            
            if result.modified_count > 0:
                print(f"✅ Executive report updated successfully: {report_id}")
                return True
            else:
                print(f"⚠️ No executive report found to update: {report_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating executive report: {e}")
            return False
    
    def update_cultural_sensitivity_analysis(self, analysis_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update cultural sensitivity analysis
        
        Args:
            analysis_id: Analysis identifier
            updates: Fields to update
            
        Returns:
            True if successful, False otherwise
        """
        if self.cultural_sensitivity_collection is None:
            return False
        
        try:
            updates["updated_at"] = datetime.now().isoformat()
            result = self.cultural_sensitivity_collection.update_one(
                {"analysis_id": analysis_id},
                {"$set": updates}
            )
            
            if result.modified_count > 0:
                print(f"✅ Cultural sensitivity analysis updated successfully: {analysis_id}")
                return True
            else:
                print(f"⚠️ No cultural sensitivity analysis found to update: {analysis_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating cultural sensitivity analysis: {e}")
            return False
    
    def delete_executive_report(self, report_id: str) -> bool:
        """
        Delete executive report (soft delete)
        
        Args:
            report_id: Report identifier
            
        Returns:
            True if successful, False otherwise
        """
        if self.executive_reports_collection is None:
            return False
        
        try:
            result = self.executive_reports_collection.update_one(
                {"report_id": report_id},
                {"$set": {"status": "deleted", "deleted_at": datetime.now().isoformat()}}
            )
            
            if result.modified_count > 0:
                print(f"✅ Executive report deleted successfully: {report_id}")
                return True
            else:
                print(f"⚠️ No executive report found to delete: {report_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting executive report: {e}")
            return False
    
    def delete_cultural_sensitivity_analysis(self, analysis_id: str) -> bool:
        """
        Delete cultural sensitivity analysis (soft delete)
        
        Args:
            analysis_id: Analysis identifier
            
        Returns:
            True if successful, False otherwise
        """
        if self.cultural_sensitivity_collection is None:
            return False
        
        try:
            result = self.cultural_sensitivity_collection.update_one(
                {"analysis_id": analysis_id},
                {"$set": {"status": "deleted", "deleted_at": datetime.now().isoformat()}}
            )
            
            if result.modified_count > 0:
                print(f"✅ Cultural sensitivity analysis deleted successfully: {analysis_id}")
                return True
            else:
                print(f"⚠️ No cultural sensitivity analysis found to delete: {analysis_id}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting cultural sensitivity analysis: {e}")
            return False
    
    def get_all_executive_reports(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all active executive reports
        
        Args:
            limit: Maximum number of reports to return
            
        Returns:
            List of executive report documents
        """
        if self.executive_reports_collection is None:
            return []
        
        try:
            cursor: Cursor = self.executive_reports_collection.find({"status": "active"}).sort("generated_at", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error retrieving executive reports: {e}")
            return []
    
    def get_all_cultural_sensitivity_analyses(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all active cultural sensitivity analyses
        
        Args:
            limit: Maximum number of analyses to return
            
        Returns:
            List of cultural sensitivity analysis documents
        """
        if self.cultural_sensitivity_collection is None:
            return []
        
        try:
            cursor: Cursor = self.cultural_sensitivity_collection.find({"status": "active"}).sort("stored_at", -1).limit(limit)
            return list(cursor)
        except Exception as e:
            print(f"❌ Error retrieving cultural sensitivity analyses: {e}")
            return []
    
    def search_executive_reports(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search executive reports by text
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching executive report documents
        """
        if self.executive_reports_collection is None:
            return []
        
        try:
            cursor: Cursor = self.executive_reports_collection.find({
                "$or": [
                    {"prd_name": {"$regex": query, "$options": "i"}},
                    {"executive_summary": {"$regex": query, "$options": "i"}},
                    {"key_findings": {"$regex": query, "$options": "i"}}
                ],
                "status": "active"
            }).sort("generated_at", -1).limit(limit)
            
            return list(cursor)
        except Exception as e:
            print(f"❌ Error searching executive reports: {e}")
            return []
    
    def search_cultural_sensitivity_analyses(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search cultural sensitivity analyses by text
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching cultural sensitivity analysis documents
        """
        if self.cultural_sensitivity_collection is None:
            return []
        
        try:
            cursor: Cursor = self.cultural_sensitivity_collection.find({
                "$or": [
                    {"overall_cultural_sensitivity": {"$regex": query, "$options": "i"}},
                    {"key_cultural_issues": {"$regex": query, "$options": "i"}},
                    {"recommendations": {"$regex": query, "$options": "i"}}
                ],
                "status": "active"
            }).sort("stored_at", -1).limit(limit)
            
            return list(cursor)
        except Exception as e:
            print(f"❌ Error searching cultural sensitivity analyses: {e}")
            return []
    
    def __del__(self):
        """Cleanup MongoDB connection"""
        if self.mongo_client:
            self.mongo_client.close()
