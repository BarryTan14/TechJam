
from fastapi import FastAPI, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import logging
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection from environment variables
uri = os.getenv("MONGODB_URI")
if not uri:
    print("⚠️  MONGODB_URI environment variable is not set - running in offline mode")
    uri = None

# Database name from environment variables
database_name = os.getenv("DATABASE_NAME", "TechJam")

# Create a new client and connect to the server
if uri:
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        db = client[database_name]
        print(f"✅ Connected to database: {db.name}")
        
        # Initialize collections
        prd_collection = db["PRD"]
        feature_data_collection = db["feature_data"]
        logs_collection = db["logs"]
        
        # Create indexes for better performance
        prd_collection.create_index("ID", unique=True)
        feature_data_collection.create_index("uuid", unique=True)
        feature_data_collection.create_index("prd_uuid")
        logs_collection.create_index("prd_uuid")
        
        MONGODB_CONNECTED = True
        print("✅ MongoDB collections initialized successfully!")
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("⚠️  Running in offline mode - API will work but data won't be persisted")
        print("💡 Check your internet connection and MongoDB Atlas settings")
        
        # Set up offline mode
        MONGODB_CONNECTED = False
        client = None
        db = None
        prd_collection = None
        feature_data_collection = None
        logs_collection = None
else:
    print("⚠️  Running in offline mode - API will work but data won't be persisted")
    MONGODB_CONNECTED = False
    client = None
    db = None
    prd_collection = None
    feature_data_collection = None
    logs_collection = None
    
    # Create mock collections for offline mode
    class MockCollection:
        def __init__(self, name):
            self.name = name
            self.data = []
        
        def insert_one(self, doc):
            doc['_id'] = len(self.data) + 1
            self.data.append(doc)
            return type('MockResult', (), {'inserted_id': doc['_id']})()
        
        def find_one(self, query):
            for doc in self.data:
                if all(doc.get(k) == v for k, v in query.items()):
                    return doc
            return None
        
        def find(self, query=None, projection=None):
            if query is None:
                return self.data
            # Simple mock filtering
            filtered = []
            for doc in self.data:
                if all(doc.get(k) == v for k, v in query.items()):
                    filtered.append(doc)
            return filtered
        
        def update_one(self, query, update):
            for i, doc in enumerate(self.data):
                if all(doc.get(k) == v for k, v in query.items()):
                    if '$set' in update:
                        for key, value in update['$set'].items():
                            doc[key] = value
                    return type('MockResult', (), {'modified_count': 1})()
            return type('MockResult', (), {'modified_count': 0})()
        
        def delete_one(self, query):
            for i, doc in enumerate(self.data):
                if all(doc.get(k) == v for k, v in query.items()):
                    del self.data[i]
                    return type('MockResult', (), {'deleted_count': 1})()
            return type('MockResult', (), {'deleted_count': 0})()
        
        def delete_many(self, query):
            deleted_count = 0
            indices_to_delete = []
            for i, doc in enumerate(self.data):
                if all(doc.get(k) == v for k, v in query.items()):
                    indices_to_delete.append(i)
                    deleted_count += 1
            
            # Delete in reverse order to avoid index shifting
            for i in reversed(indices_to_delete):
                del self.data[i]
            
            return type('MockResult', (), {'deleted_count': deleted_count})()
        
        def count_documents(self, query):
            if query is None or query == {}:
                return len(self.data)
            count = 0
            for doc in self.data:
                if all(doc.get(k) == v for k, v in query.items()):
                    count += 1
            return count
        
        def sort(self, field, direction=1):
            # Simple sorting for mock collection
            if field == "timestamp":
                # Sort by timestamp if it exists, otherwise keep original order
                self.data.sort(key=lambda x: x.get(field, 0), reverse=(direction == -1))
            return self
        
        def create_index(self, field, **kwargs):
            # Mock index creation
            pass
    
    # Initialize mock collections
    prd_collection = MockCollection("PRD")
    feature_data_collection = MockCollection("feature_data")
    logs_collection = MockCollection("logs")

# Data migration function
def migrate_existing_data():
    """Migrate existing data to include timestamp fields"""
    try:
        if not MONGODB_CONNECTED:
            return  # Skip migration in offline mode
        
        current_time = get_current_timestamp()
        migrated_count = 0
        
        # Migrate PRDs
        prds_without_timestamps = prd_collection.find({
            "$or": [
                {"created_at": {"$exists": False}},
                {"updated_at": {"$exists": False}}
            ]
        })
        
        for prd in prds_without_timestamps:
            update_data = {}
            if 'created_at' not in prd:
                update_data['created_at'] = current_time
            if 'updated_at' not in prd:
                update_data['updated_at'] = current_time
            
            if update_data:
                prd_collection.update_one(
                    {"_id": prd["_id"]},
                    {"$set": update_data}
                )
                migrated_count += 1
        
        # Migrate feature data
        features_without_timestamps = feature_data_collection.find({
            "$or": [
                {"created_at": {"$exists": False}},
                {"updated_at": {"$exists": False}}
            ]
        })
        
        for feature in features_without_timestamps:
            update_data = {}
            if 'created_at' not in feature:
                update_data['created_at'] = current_time
            if 'updated_at' not in feature:
                update_data['updated_at'] = current_time
            
            if update_data:
                feature_data_collection.update_one(
                    {"_id": feature["_id"]},
                    {"$set": update_data}
                )
                migrated_count += 1
        
        # Migrate logs
        logs_without_timestamps = logs_collection.find({
            "timestamp": {"$exists": False}
        })
        
        for log in logs_without_timestamps:
            logs_collection.update_one(
                {"_id": log["_id"]},
                {"$set": {"timestamp": current_time}}
            )
            migrated_count += 1
        
        if migrated_count > 0:
            print(f"✅ Migrated {migrated_count} documents to include timestamp fields")
        
    except Exception as e:
        print(f"⚠️  Data migration failed: {e}")
        # Continue without migration

# Pydantic models
class PRDBase(BaseModel):
    Name: str = Field(..., description="PRD Name")
    Description: str = Field(..., description="PRD Description")
    Status: str = Field(default="Draft", description="PRD Status")

class PRDCreate(PRDBase):
    pass

class PRDUpdate(BaseModel):
    Name: Optional[str] = None
    Description: Optional[str] = None
    Status: Optional[str] = None

class PRDResponse(PRDBase):
    ID: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # LangGraph analysis fields
    langgraph_analysis: Optional[Dict[str, Any]] = None

class FeatureDataBase(BaseModel):
    prd_uuid: str = Field(..., description="UUID from PRD table")
    data: dict = Field(..., description="Feature data content")

class FeatureDataCreate(FeatureDataBase):
    pass

class FeatureDataUpdate(BaseModel):
    prd_uuid: Optional[str] = None
    data: Optional[dict] = None

class FeatureDataResponse(FeatureDataBase):
    uuid: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class LogBase(BaseModel):
    prd_uuid: str = Field(..., description="UUID from PRD table")
    action: str = Field(..., description="Action performed")
    details: str = Field(..., description="Log details")
    level: str = Field(default="INFO", description="Log level")

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    uuid: str
    timestamp: Optional[datetime] = None

# LangGraph API Models
class LangGraphRequest(BaseModel):
    name: str = Field(..., description="PRD Name")
    description: str = Field(..., description="PRD Description")
    content: Optional[str] = Field(None, description="PRD Content (optional)")

class LangGraphResponse(BaseModel):
    workflow_id: str
    prd_name: str
    prd_description: str
    overall_risk_level: str
    overall_confidence_score: float
    total_features_analyzed: int
    critical_compliance_issues: List[str]
    summary_recommendations: List[str]
    non_compliant_states: Dict[str, Any]
    processing_time: float
    status: str = "completed"



# Create API router
api_router = APIRouter(prefix="/api")

# FastAPI app
app = FastAPI(
    title="TechJam Backend API",
    description="CRUD operations for TechJam MongoDB collections",
    version="1.0.0"
)

# Add CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def generate_uuid():
    return str(uuid.uuid4())

def get_current_timestamp():
    return datetime.utcnow()

def ensure_timestamps(data: dict) -> dict:
    """Ensure all required timestamp fields are present"""
    current_time = get_current_timestamp()
    
    # Ensure created_at exists
    if 'created_at' not in data or data['created_at'] is None:
        data['created_at'] = current_time
    
    # Ensure updated_at exists
    if 'updated_at' not in data or data['updated_at'] is None:
        data['updated_at'] = current_time
    
    # For logs, ensure timestamp exists
    if 'timestamp' not in data or data['timestamp'] is None:
        data['timestamp'] = current_time
    
    return data

# Run data migration for existing data
migrate_existing_data()

# PRD CRUD Operations
@api_router.post("/prd", response_model=PRDResponse, status_code=status.HTTP_201_CREATED)
async def create_prd(prd: PRDCreate):
    """Create a new PRD and run LangGraph analysis"""
    try:
        # Generate unique ID
        prd_id = generate_uuid()
        current_time = get_current_timestamp()
        
        prd_data = {
            "ID": prd_id,
            "Name": prd.Name,
            "Description": prd.Description,
            "Status": prd.Status,
            "created_at": current_time,
            "updated_at": current_time
        }
        
        # Save PRD to database
        result = prd_collection.insert_one(prd_data)
        
        # Log the PRD creation
        log_data = {
            "uuid": generate_uuid(),
            "prd_uuid": prd_id,
            "action": "CREATE",
            "details": f"PRD '{prd.Name}' created",
            "level": "INFO",
            "timestamp": current_time
        }
        logs_collection.insert_one(log_data)
        
        logger.info(f"PRD created: {prd_id}")
        
        # Call LangGraph API for analysis
        try:
            logger.info(f"🔍 Starting LangGraph analysis for PRD: {prd.Name}")
            
            # Get LangGraph API URL from environment
            langgraph_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:8000")
            
            # Prepare request data for LangGraph
            langgraph_request_data = {
                "name": prd.Name,
                "description": prd.Description,
                "content": None  # Let LangGraph generate content if needed
            }
            
            # Call LangGraph API
            async with httpx.AsyncClient(timeout=None) as client:  # No timeout - wait indefinitely
                response = await client.post(
                    f"{langgraph_url}/analyze-prd",
                    json=langgraph_request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    # Parse LangGraph response
                    langgraph_result = response.json()
                    
                    # Prepare analysis data to save in PRD
                    analysis_data = {
                        "workflow_id": langgraph_result.get("workflow_id"),
                        "overall_risk_level": langgraph_result.get("overall_risk_level"),
                        "overall_confidence_score": langgraph_result.get("overall_confidence_score"),
                        "total_features_analyzed": langgraph_result.get("total_features_analyzed"),
                        "critical_compliance_issues": langgraph_result.get("critical_compliance_issues", []),
                        "summary_recommendations": langgraph_result.get("summary_recommendations", []),
                        "non_compliant_states": langgraph_result.get("non_compliant_states", {}),
                        "processing_time": langgraph_result.get("processing_time"),
                        "analysis_timestamp": current_time,
                        "status": "completed"
                    }
                    
                    # Update PRD with analysis results
                    prd_collection.update_one(
                        {"ID": prd_id},
                        {"$set": {"langgraph_analysis": analysis_data}}
                    )
                    
                    # Create feature records from feature_compliance_results
                    feature_compliance_results = langgraph_result.get("feature_compliance_results", [])
                    if feature_compliance_results:
                        logger.info(f"📋 Creating {len(feature_compliance_results)} feature records for PRD: {prd.Name}")
                        
                        for feature_result in feature_compliance_results:
                            try:
                                feature = feature_result.get("feature", {})
                                
                                # Prepare feature data
                                feature_data = {
                                    "uuid": generate_uuid(),
                                    "prd_uuid": prd_id,
                                    "data": {
                                        "feature_id": feature.get("feature_id"),
                                        "feature_name": feature.get("feature_name"),
                                        "feature_description": feature.get("feature_description"),
                                        "feature_content": feature.get("feature_content"),
                                        "section": feature.get("section"),
                                        "priority": feature.get("priority"),
                                        "complexity": feature.get("complexity"),
                                        "data_types": feature.get("data_types", []),
                                        "user_impact": feature.get("user_impact"),
                                        "technical_requirements": feature.get("technical_requirements", []),
                                        "compliance_considerations": feature.get("compliance_considerations", []),
                                        # Compliance analysis results
                                        "compliance_flags": feature_result.get("compliance_flags", []),
                                        "risk_level": feature_result.get("risk_level"),
                                        "confidence_score": feature_result.get("confidence_score"),
                                        "requires_human_review": feature_result.get("requires_human_review", False),
                                        "reasoning": feature_result.get("reasoning"),
                                        "recommendations": feature_result.get("recommendations", []),
                                        "non_compliant_states": feature_result.get("non_compliant_states", []),
                                        "state_compliance_scores": feature_result.get("state_compliance_scores", {}),
                                        "processing_time": feature_result.get("processing_time"),
                                        "analysis_timestamp": feature_result.get("timestamp")
                                    },
                                    "created_at": current_time,
                                    "updated_at": current_time
                                }
                                
                                # Insert feature record
                                feature_data_collection.insert_one(feature_data)
                                
                                # Log feature creation
                                feature_log_data = {
                                    "uuid": generate_uuid(),
                                    "prd_uuid": prd_id,
                                    "action": "CREATE_FEATURE_FROM_LANGGRAPH",
                                    "details": f"Feature '{feature.get('feature_name', 'Unknown')}' created from LangGraph analysis",
                                    "level": "INFO",
                                    "timestamp": current_time
                                }
                                logs_collection.insert_one(feature_log_data)
                                
                                logger.info(f"✅ Feature created: {feature.get('feature_name', 'Unknown')} (Risk: {feature_result.get('risk_level', 'unknown')})")
                                
                            except Exception as feature_error:
                                logger.error(f"❌ Error creating feature record: {feature_error}")
                                # Log the feature creation error
                                error_log_data = {
                                    "uuid": generate_uuid(),
                                    "prd_uuid": prd_id,
                                    "action": "FEATURE_CREATION_ERROR",
                                    "details": f"Failed to create feature record: {str(feature_error)}",
                                    "level": "ERROR",
                                    "timestamp": current_time
                                }
                                logs_collection.insert_one(error_log_data)
                        
                        logger.info(f"📊 Successfully created {len(feature_compliance_results)} feature records for PRD: {prd.Name}")
                    else:
                        logger.info(f"⚠️ No feature_compliance_results found in LangGraph response for PRD: {prd.Name}")
                    
                    # Log the successful analysis
                    analysis_log_data = {
                        "uuid": generate_uuid(),
                        "prd_uuid": prd_id,
                        "action": "LANGGRAPH_ANALYSIS_COMPLETED",
                        "details": f"LangGraph analysis completed for PRD '{prd.Name}'. Risk: {langgraph_result.get('overall_risk_level', 'unknown')}",
                        "level": "INFO",
                        "timestamp": current_time
                    }
                    logs_collection.insert_one(analysis_log_data)
                    
                    logger.info(f"✅ LangGraph analysis completed for PRD: {prd.Name}")
                    logger.info(f"📊 Risk Level: {langgraph_result.get('overall_risk_level', 'unknown').upper()}")
                    logger.info(f"⏱️ Processing Time: {langgraph_result.get('processing_time', 0):.2f}s")
                    
                else:
                    # Log LangGraph API error
                    error_log_data = {
                        "uuid": generate_uuid(),
                        "prd_uuid": prd_id,
                        "action": "LANGGRAPH_ANALYSIS_FAILED",
                        "details": f"LangGraph API error: {response.status_code} - {response.text}",
                        "level": "ERROR",
                        "timestamp": current_time
                    }
                    logs_collection.insert_one(error_log_data)
                    
                    logger.error(f"❌ LangGraph API error: {response.status_code} - {response.text}")
                    
        except httpx.TimeoutException:
            # Log timeout error
            timeout_log_data = {
                "uuid": generate_uuid(),
                "prd_uuid": prd_id,
                "action": "LANGGRAPH_ANALYSIS_TIMEOUT",
                "details": f"LangGraph analysis timed out for PRD '{prd.Name}'",
                "level": "WARNING",
                "timestamp": current_time
            }
            logs_collection.insert_one(timeout_log_data)
            
            logger.warning(f"⏰ LangGraph analysis timed out for PRD: {prd.Name}")
            
        except httpx.ConnectError:
            # Log connection error
            connection_log_data = {
                "uuid": generate_uuid(),
                "prd_uuid": prd_id,
                "action": "LANGGRAPH_ANALYSIS_CONNECTION_ERROR",
                "details": f"Cannot connect to LangGraph API for PRD '{prd.Name}'",
                "level": "WARNING",
                "timestamp": current_time
            }
            logs_collection.insert_one(connection_log_data)
            
            logger.warning(f"🔌 Cannot connect to LangGraph API for PRD: {prd.Name}")
            
        except Exception as e:
            # Log general error
            error_log_data = {
                "uuid": generate_uuid(),
                "prd_uuid": prd_id,
                "action": "LANGGRAPH_ANALYSIS_ERROR",
                "details": f"LangGraph analysis error for PRD '{prd.Name}': {str(e)}",
                "level": "ERROR",
                "timestamp": current_time
            }
            logs_collection.insert_one(error_log_data)
            
            logger.error(f"❌ LangGraph analysis error for PRD {prd.Name}: {e}")
        
        # Get the final PRD data (including analysis if completed)
        final_prd = prd_collection.find_one({"ID": prd_id}, {"_id": 0})
        ensure_timestamps(final_prd)
        
        # Return the PRD response (including analysis if completed)
        return PRDResponse(**final_prd)
        
    except Exception as e:
        logger.error(f"Error creating PRD: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create PRD: {str(e)}")

@api_router.get("/prd", response_model=List[PRDResponse])
async def get_all_prds():
    """Get all PRDs"""
    try:
        prds = list(prd_collection.find({}, {"_id": 0}))
        # Ensure all PRDs have required timestamp fields
        for prd in prds:
            ensure_timestamps(prd)
        logger.info(f"Retrieved {len(prds)} PRDs")
        return prds
    except Exception as e:
        logger.error(f"Error retrieving PRDs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve PRDs: {str(e)}")

@api_router.get("/prd/{prd_id}", response_model=PRDResponse)
async def get_prd(prd_id: str):
    """Get a specific PRD by ID"""
    try:
        prd = prd_collection.find_one({"ID": prd_id}, {"_id": 0})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        # Ensure PRD has required timestamp fields
        ensure_timestamps(prd)
        
        logger.info(f"Retrieved PRD: {prd_id}")
        return prd
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving PRD {prd_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve PRD: {str(e)}")

@api_router.get("/prd/{prd_id}/dashboard")
async def get_prd_dashboard(prd_id: str):
    """Get PRD and its associated features for dashboard view"""
    try:
        # Get PRD
        prd = prd_collection.find_one({"ID": prd_id}, {"_id": 0})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        # Ensure PRD has required timestamp fields
        ensure_timestamps(prd)
        
        # Get features for this PRD
        features = list(feature_data_collection.find({"prd_uuid": prd_id}, {"_id": 0}))
        # Ensure all features have required timestamp fields
        for feature in features:
            ensure_timestamps(feature)
        
        # Prepare dashboard response
        dashboard_data = {
            "prd": prd,
            "features": features,
            "total_features": len(features),
            "features_with_high_risk": len([f for f in features if f.get('data', {}).get('risk_level') == 'high']),
            "features_with_medium_risk": len([f for f in features if f.get('data', {}).get('risk_level') == 'medium']),
            "features_with_low_risk": len([f for f in features if f.get('data', {}).get('risk_level') == 'low'])
        }
        
        logger.info(f"Dashboard data retrieved for PRD: {prd_id} with {len(features)} features")
        return dashboard_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving dashboard data for PRD {prd_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard data: {str(e)}")

@api_router.put("/prd/{prd_id}", response_model=PRDResponse)
async def update_prd(prd_id: str, prd_update: PRDUpdate):
    """Update a PRD"""
    try:
        # Check if PRD exists
        existing_prd = prd_collection.find_one({"ID": prd_id})
        if not existing_prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        # Prepare update data
        update_data = {}
        if prd_update.Name is not None:
            update_data["Name"] = prd_update.Name
        if prd_update.Description is not None:
            update_data["Description"] = prd_update.Description
        if prd_update.Status is not None:
            update_data["Status"] = prd_update.Status
        
        update_data["updated_at"] = get_current_timestamp()
        
        # Update PRD
        result = prd_collection.update_one(
            {"ID": prd_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made")
        
        # Log the update
        log_data = {
            "uuid": generate_uuid(),
            "prd_uuid": prd_id,
            "action": "UPDATE",
            "details": f"PRD '{prd_id}' updated",
            "level": "INFO",
            "timestamp": get_current_timestamp()
        }
        logs_collection.insert_one(log_data)
        
        # Return updated PRD
        updated_prd = prd_collection.find_one({"ID": prd_id}, {"_id": 0})
        logger.info(f"PRD updated: {prd_id}")
        return updated_prd
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating PRD {prd_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update PRD: {str(e)}")

@api_router.delete("/prd/{prd_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prd(prd_id: str):
    """Delete a PRD"""
    try:
        # Check if PRD exists
        existing_prd = prd_collection.find_one({"ID": prd_id})
        if not existing_prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        # Delete PRD
        result = prd_collection.delete_one({"ID": prd_id})
        
        # Delete related feature data
        feature_data_collection.delete_many({"prd_uuid": prd_id})
        
        # Log the deletion
        log_data = {
            "uuid": generate_uuid(),
            "prd_uuid": prd_id,
            "action": "DELETE",
            "details": f"PRD '{prd_id}' deleted",
            "level": "WARNING",
            "timestamp": get_current_timestamp()
        }
        logs_collection.insert_one(log_data)
        
        logger.info(f"PRD deleted: {prd_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting PRD {prd_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete PRD: {str(e)}")

# Feature Data CRUD Operations
@api_router.post("/feature-data", response_model=FeatureDataResponse, status_code=status.HTTP_201_CREATED)
async def create_feature_data(feature_data: FeatureDataCreate):
    """Create new feature data"""
    try:
        # Verify PRD exists
        prd = prd_collection.find_one({"ID": feature_data.prd_uuid})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        feature_uuid = generate_uuid()
        current_time = get_current_timestamp()
        
        feature_data_doc = {
            "uuid": feature_uuid,
            "prd_uuid": feature_data.prd_uuid,
            "data": feature_data.data,
            "created_at": current_time,
            "updated_at": current_time
        }
        
        result = feature_data_collection.insert_one(feature_data_doc)
        
        # Log the creation
        log_data = {
            "uuid": generate_uuid(),
            "prd_uuid": feature_data.prd_uuid,
            "action": "CREATE_FEATURE_DATA",
            "details": f"Feature data created for PRD {feature_data.prd_uuid}",
            "level": "INFO",
            "timestamp": current_time
        }
        logs_collection.insert_one(log_data)
        
        logger.info(f"Feature data created: {feature_uuid}")
        return FeatureDataResponse(**feature_data_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating feature data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create feature data: {str(e)}")

@api_router.get("/feature-data", response_model=List[FeatureDataResponse])
async def get_all_feature_data():
    """Get all feature data"""
    try:
        feature_data = list(feature_data_collection.find({}, {"_id": 0}))
        # Ensure all feature data have required timestamp fields
        for feature in feature_data:
            ensure_timestamps(feature)
        logger.info(f"Retrieved {len(feature_data)} feature data records")
        return feature_data
    except Exception as e:
        logger.error(f"Error retrieving feature data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve feature data: {str(e)}")

@api_router.get("/feature-data/{uuid}", response_model=FeatureDataResponse)
async def get_feature_data(uuid: str):
    """Get specific feature data by UUID"""
    try:
        feature_data = feature_data_collection.find_one({"uuid": uuid}, {"_id": 0})
        if not feature_data:
            raise HTTPException(status_code=404, detail="Feature data not found")
        
        # Ensure feature data has required timestamp fields
        ensure_timestamps(feature_data)
        
        logger.info(f"Retrieved feature data: {uuid}")
        return feature_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving feature data {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve feature data: {str(e)}")

@api_router.get("/feature-data/prd/{prd_uuid}", response_model=List[FeatureDataResponse])
async def get_feature_data_by_prd(prd_uuid: str):
    """Get all feature data for a specific PRD"""
    try:
        # Verify PRD exists
        prd = prd_collection.find_one({"ID": prd_uuid})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        feature_data = list(feature_data_collection.find({"prd_uuid": prd_uuid}, {"_id": 0}))
        # Ensure all feature data have required timestamp fields
        for feature in feature_data:
            ensure_timestamps(feature)
        logger.info(f"Retrieved {len(feature_data)} feature data records for PRD {prd_uuid}")
        return feature_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving feature data for PRD {prd_uuid}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve feature data: {str(e)}")

@api_router.put("/feature-data/{uuid}", response_model=FeatureDataResponse)
async def update_feature_data(uuid: str, feature_data_update: FeatureDataUpdate):
    """Update feature data"""
    try:
        # Check if feature data exists
        existing_feature_data = feature_data_collection.find_one({"uuid": uuid})
        if not existing_feature_data:
            raise HTTPException(status_code=404, detail="Feature data not found")
        
        # Prepare update data
        update_data = {}
        if feature_data_update.prd_uuid is not None:
            # Verify new PRD exists
            prd = prd_collection.find_one({"ID": feature_data_update.prd_uuid})
            if not prd:
                raise HTTPException(status_code=404, detail="New PRD not found")
            update_data["prd_uuid"] = feature_data_update.prd_uuid
            
        if feature_data_update.data is not None:
            update_data["data"] = feature_data_update.data
        
        update_data["updated_at"] = get_current_timestamp()
        
        # Update feature data
        result = feature_data_collection.update_one(
            {"uuid": uuid},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made")
        
        # Log the update
        log_data = {
            "uuid": generate_uuid(),
            "prd_uuid": existing_feature_data["prd_uuid"],
            "action": "UPDATE_FEATURE_DATA",
            "details": f"Feature data {uuid} updated",
            "level": "INFO",
            "timestamp": get_current_timestamp()
        }
        logs_collection.insert_one(log_data)
        
        # Return updated feature data
        updated_feature_data = feature_data_collection.find_one({"uuid": uuid}, {"_id": 0})
        logger.info(f"Feature data updated: {uuid}")
        return updated_feature_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating feature data {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update feature data: {str(e)}")

@api_router.delete("/feature-data/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature_data(uuid: str):
    """Delete feature data"""
    try:
        # Check if feature data exists
        existing_feature_data = feature_data_collection.find_one({"uuid": uuid})
        if not existing_feature_data:
            raise HTTPException(status_code=404, detail="Feature data not found")
        
        # Delete feature data
        result = feature_data_collection.delete_one({"uuid": uuid})
        
        # Log the deletion
        log_data = {
            "uuid": generate_uuid(),
            "prd_uuid": existing_feature_data["prd_uuid"],
            "action": "DELETE_FEATURE_DATA",
            "details": f"Feature data {uuid} deleted",
            "level": "WARNING",
            "timestamp": get_current_timestamp()
        }
        logs_collection.insert_one(log_data)
        
        logger.info(f"Feature data deleted: {uuid}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting feature data {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete feature data: {str(e)}")

# Logs CRUD Operations
@api_router.post("/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
async def create_log(log: LogCreate):
    """Create a new log entry"""
    try:
        # Verify PRD exists
        prd = prd_collection.find_one({"ID": log.prd_uuid})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        log_uuid = generate_uuid()
        current_time = get_current_timestamp()
        
        log_doc = {
            "uuid": log_uuid,
            "prd_uuid": log.prd_uuid,
            "action": log.action,
            "details": log.details,
            "level": log.level,
            "timestamp": current_time
        }
        
        result = logs_collection.insert_one(log_doc)
        
        logger.info(f"Log created: {log_uuid}")
        return LogResponse(**log_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating log: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create log: {str(e)}")

@api_router.get("/logs", response_model=List[LogResponse])
async def get_all_logs():
    """Get all logs"""
    try:
        logs = list(logs_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        # Ensure all logs have required timestamp fields
        for log in logs:
            ensure_timestamps(log)
        logger.info(f"Retrieved {len(logs)} log entries")
        return logs
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@api_router.get("/logs/{uuid}", response_model=LogResponse)
async def get_log(uuid: str):
    """Get a specific log by UUID"""
    try:
        log = logs_collection.find_one({"uuid": uuid}, {"_id": 0})
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        
        # Ensure log has required timestamp fields
        ensure_timestamps(log)
        
        logger.info(f"Retrieved log: {uuid}")
        return log
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving log {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve log: {str(e)}")

@api_router.get("/logs/prd/{prd_uuid}", response_model=List[LogResponse])
async def get_logs_by_prd(prd_uuid: str):
    """Get all logs for a specific PRD"""
    try:
        # Verify PRD exists
        prd = prd_collection.find_one({"ID": prd_uuid})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        logs = list(logs_collection.find({"prd_uuid": prd_uuid}, {"_id": 0}).sort("timestamp", -1))
        # Ensure all logs have required timestamp fields
        for log in logs:
            ensure_timestamps(log)
        logger.info(f"Retrieved {len(logs)} log entries for PRD {prd_uuid}")
        return logs
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving logs for PRD {prd_uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@api_router.delete("/logs/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(uuid: str):
    """Delete a log entry"""
    try:
        # Check if log exists
        existing_log = logs_collection.find_one({"uuid": uuid})
        if not existing_log:
            raise HTTPException(status_code=404, detail="Log not found")
        
        # Delete log
        result = logs_collection.delete_one({"uuid": uuid})
        
        logger.info(f"Log deleted: {uuid}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting log {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete log: {str(e)}")

# LangGraph Integration
@api_router.post("/langgraph/analyze", response_model=LangGraphResponse, status_code=status.HTTP_200_OK)
async def analyze_prd_with_langgraph(request: LangGraphRequest):
    """
    Analyze a PRD using the LangGraph compliance workflow
    
    This endpoint calls the LangGraph API to perform comprehensive compliance analysis
    of a PRD, including risk assessment, compliance issues, and recommendations.
    """
    try:
        # Get LangGraph API URL from environment
        langgraph_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:8000")
        
        logger.info(f"🔍 Calling LangGraph API for PRD analysis: {request.name}")
        
        # Prepare request data
        langgraph_request_data = {
            "name": request.name,
            "description": request.description,
            "content": request.content
        }
        
        # Call LangGraph API
        async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minute timeout
            response = await client.post(
                f"{langgraph_url}/analyze-prd",
                json=langgraph_request_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                logger.error(f"LangGraph API error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"LangGraph API error: {response.text}"
                )
            
            # Parse response
            langgraph_result = response.json()
            
            # Log the analysis
            log_data = {
                "uuid": generate_uuid(),
                "prd_uuid": request.name,  # Using name as identifier for now
                "action": "LANGGRAPH_ANALYSIS",
                "details": f"PRD '{request.name}' analyzed with LangGraph. Risk: {langgraph_result.get('overall_risk_level', 'unknown')}",
                "level": "INFO",
                "timestamp": get_current_timestamp()
            }
            logs_collection.insert_one(log_data)
            
            logger.info(f"✅ LangGraph analysis completed for: {request.name}")
            logger.info(f"📊 Risk Level: {langgraph_result.get('overall_risk_level', 'unknown').upper()}")
            logger.info(f"⏱️ Processing Time: {langgraph_result.get('processing_time', 0):.2f}s")
            
            return LangGraphResponse(**langgraph_result)
            
    except httpx.TimeoutException:
        logger.error(f"❌ LangGraph API timeout for PRD: {request.name}")
        raise HTTPException(
            status_code=408,
            detail="LangGraph analysis timed out. Please try again."
        )
    except httpx.ConnectError:
        logger.error(f"❌ Cannot connect to LangGraph API")
        raise HTTPException(
            status_code=503,
            detail="LangGraph service is unavailable. Please check if the LangGraph server is running."
        )
    except Exception as e:
        logger.error(f"❌ Error calling LangGraph API: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze PRD with LangGraph: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        if MONGODB_CONNECTED:
            # Test MongoDB connection
            client.admin.command('ping')
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": get_current_timestamp().isoformat(),
                "collections": {
                    "PRD": prd_collection.count_documents({}),
                    "feature_data": feature_data_collection.count_documents({}),
                    "logs": logs_collection.count_documents({})
                },
                "features_per_prd": {
                    "total_features": feature_data_collection.count_documents({}),
                    "prds_with_features": len(prd_collection.distinct("ID", {"langgraph_analysis": {"$exists": True}}))
                }
            }
        else:
            # Offline mode
            return {
                "status": "healthy",
                "database": "offline",
                "mode": "mock_data",
                "timestamp": get_current_timestamp().isoformat(),
                "collections": {
                    "PRD": prd_collection.count_documents({}),
                    "feature_data": feature_data_collection.count_documents({}),
                    "logs": logs_collection.count_documents({})
                },
                "features_per_prd": {
                    "total_features": feature_data_collection.count_documents({}),
                    "prds_with_features": len(prd_collection.distinct("ID", {"langgraph_analysis": {"$exists": True}}))
                },
                "note": "Running in offline mode - data is not persisted"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TechJam Backend API",
        "version": "1.0.0",
        "status": "running",
        "port": 5000,
        "database": "connected" if MONGODB_CONNECTED else "offline",
        "mode": "production" if MONGODB_CONNECTED else "mock_data",
        "collections": ["PRD", "feature_data", "logs"],
        "docs": "/docs",
        "note": "Data persistence available" if MONGODB_CONNECTED else "Running in offline mode - data not persisted"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))
    
    print("🚀 Starting TechJam Backend API...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    
    if MONGODB_CONNECTED:
        print("✅ MongoDB: Connected (Production Mode)")
    else:
        print("⚠️  MongoDB: Offline (Mock Data Mode)")
        print("💡 Data will be stored in memory but not persisted")
    
    print("📚 API Documentation: http://localhost:{port}/docs")
    print("🔍 Health Check: http://localhost:{port}/health")
    print("🌐 API Base URL: http://localhost:{port}")
    print("⏹️  Press Ctrl+C to stop")
    
    # Include API router after all endpoints are defined
    app.include_router(api_router)
    
    uvicorn.run(app, host=host, port=port)