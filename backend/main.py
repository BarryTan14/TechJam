
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
uri = "mongodb+srv://tanedric_db_user:vZkI4o5u3VnKvThk@techjam.8cvwszr.mongodb.net/?retryWrites=true&w=majority&appName=TechJam"

# Create a new client and connect to the server
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
    db = client["TechJam"]
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
        
        def count_documents(self, query):
            if query is None or query == {}:
                return len(self.data)
            count = 0
            for doc in self.data:
                if all(doc.get(k) == v for k, v in query.items()):
                    count += 1
            return count
        
        def create_index(self, field, **kwargs):
            # Mock index creation
            pass
    
    # Initialize mock collections
    prd_collection = MockCollection("PRD")
    feature_data_collection = MockCollection("feature_data")
    logs_collection = MockCollection("logs")

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
    created_at: datetime
    updated_at: datetime

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
    created_at: datetime
    updated_at: datetime

class LogBase(BaseModel):
    prd_uuid: str = Field(..., description="UUID from PRD table")
    action: str = Field(..., description="Action performed")
    details: str = Field(..., description="Log details")
    level: str = Field(default="INFO", description="Log level")

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    uuid: str
    timestamp: datetime

# FastAPI app
app = FastAPI(
    title="TechJam Backend API",
    description="CRUD operations for TechJam MongoDB collections",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def generate_uuid():
    return str(uuid.uuid4())

def get_current_timestamp():
    return datetime.utcnow()

# PRD CRUD Operations
@app.post("/prd", response_model=PRDResponse, status_code=status.HTTP_201_CREATED)
async def create_prd(prd: PRDCreate):
    """Create a new PRD"""
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
        
        result = prd_collection.insert_one(prd_data)
        
        # Log the creation
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
        return PRDResponse(**prd_data)
        
    except Exception as e:
        logger.error(f"Error creating PRD: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create PRD: {str(e)}")

@app.get("/prd", response_model=List[PRDResponse])
async def get_all_prds():
    """Get all PRDs"""
    try:
        prds = list(prd_collection.find({}, {"_id": 0}))
        logger.info(f"Retrieved {len(prds)} PRDs")
        return prds
    except Exception as e:
        logger.error(f"Error retrieving PRDs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve PRDs: {str(e)}")

@app.get("/prd/{prd_id}", response_model=PRDResponse)
async def get_prd(prd_id: str):
    """Get a specific PRD by ID"""
    try:
        prd = prd_collection.find_one({"ID": prd_id}, {"_id": 0})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        logger.info(f"Retrieved PRD: {prd_id}")
        return prd
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving PRD {prd_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve PRD: {str(e)}")

@app.put("/prd/{prd_id}", response_model=PRDResponse)
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

@app.delete("/prd/{prd_id}", status_code=status.HTTP_204_NO_CONTENT)
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
@app.post("/feature-data", response_model=FeatureDataResponse, status_code=status.HTTP_201_CREATED)
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

@app.get("/feature-data", response_model=List[FeatureDataResponse])
async def get_all_feature_data():
    """Get all feature data"""
    try:
        feature_data = list(feature_data_collection.find({}, {"_id": 0}))
        logger.info(f"Retrieved {len(feature_data)} feature data records")
        return feature_data
    except Exception as e:
        logger.error(f"Error retrieving feature data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve feature data: {str(e)}")

@app.get("/feature-data/{uuid}", response_model=FeatureDataResponse)
async def get_feature_data(uuid: str):
    """Get specific feature data by UUID"""
    try:
        feature_data = feature_data_collection.find_one({"uuid": uuid}, {"_id": 0})
        if not feature_data:
            raise HTTPException(status_code=404, detail="Feature data not found")
        
        logger.info(f"Retrieved feature data: {uuid}")
        return feature_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving feature data {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve feature data: {str(e)}")

@app.get("/feature-data/prd/{prd_uuid}", response_model=List[FeatureDataResponse])
async def get_feature_data_by_prd(prd_uuid: str):
    """Get all feature data for a specific PRD"""
    try:
        # Verify PRD exists
        prd = prd_collection.find_one({"ID": prd_uuid})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        feature_data = list(feature_data_collection.find({"prd_uuid": prd_uuid}, {"_id": 0}))
        logger.info(f"Retrieved {len(feature_data)} feature data records for PRD {prd_uuid}")
        return feature_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving feature data for PRD {prd_uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve feature data: {str(e)}")

@app.put("/feature-data/{uuid}", response_model=FeatureDataResponse)
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

@app.delete("/feature-data/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
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
@app.post("/logs", response_model=LogResponse, status_code=status.HTTP_201_CREATED)
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

@app.get("/logs", response_model=List[LogResponse])
async def get_all_logs():
    """Get all logs"""
    try:
        logs = list(logs_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        logger.info(f"Retrieved {len(logs)} log entries")
        return logs
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@app.get("/logs/{uuid}", response_model=LogResponse)
async def get_log(uuid: str):
    """Get a specific log by UUID"""
    try:
        log = logs_collection.find_one({"uuid": uuid}, {"_id": 0})
        if not log:
            raise HTTPException(status_code=404, detail="Log not found")
        
        logger.info(f"Retrieved log: {uuid}")
        return log
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving log {uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve log: {str(e)}")

@app.get("/logs/prd/{prd_uuid}", response_model=List[LogResponse])
async def get_logs_by_prd(prd_uuid: str):
    """Get all logs for a specific PRD"""
    try:
        # Verify PRD exists
        prd = prd_collection.find_one({"ID": prd_uuid})
        if not prd:
            raise HTTPException(status_code=404, detail="PRD not found")
        
        logs = list(logs_collection.find({"prd_uuid": prd_uuid}, {"_id": 0}).sort("timestamp", -1))
        logger.info(f"Retrieved {len(logs)} log entries for PRD {prd_uuid}")
        return logs
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving logs for PRD {prd_uuid}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve logs: {str(e)}")

@app.delete("/logs/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
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
    print("🚀 Starting TechJam Backend API on port 5000...")
    
    if MONGODB_CONNECTED:
        print("✅ MongoDB: Connected (Production Mode)")
    else:
        print("⚠️  MongoDB: Offline (Mock Data Mode)")
        print("💡 Data will be stored in memory but not persisted")
    
    print("📚 API Documentation: http://localhost:5000/docs")
    print("🔍 Health Check: http://localhost:5000/health")
    print("🌐 API Base URL: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run(app, host="0.0.0.0", port=5000)