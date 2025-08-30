from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the workflow
from langgraph_workflow import ComplianceWorkflow, WorkflowState

# Pydantic models for API
class PRDRequest(BaseModel):
    name: str = Field(..., description="PRD Name")
    description: str = Field(..., description="PRD Description")
    content: Optional[str] = Field(None, description="PRD Content (optional)")

class WorkflowResponse(BaseModel):
    workflow_id: str
    prd_name: str
    prd_description: str
    overall_risk_level: str
    overall_confidence_score: float
    total_features_analyzed: int
    critical_compliance_issues: list
    summary_recommendations: list
    non_compliant_states: Dict[str, Any]
    feature_compliance_results: list
    state_analysis_results: Dict[str, Dict[str, Any]]  # New state-centric results
    processing_time: float
    status: str = "completed"

# FastAPI app
app = FastAPI(
    title="LangGraph Compliance Workflow API",
    description="API for running PRD compliance analysis workflow",
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

# Initialize workflow
workflow = None

@app.on_event("startup")
async def startup_event():
    """Initialize the workflow on startup"""
    global workflow
    try:
        logger.info("🚀 Initializing LangGraph Compliance Workflow...")
        workflow = ComplianceWorkflow()
        logger.info("✅ Workflow initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to initialize workflow: {e}")
        raise

@app.post("/analyze-prd", response_model=WorkflowResponse, status_code=status.HTTP_200_OK)
async def analyze_prd(request: PRDRequest):
    """
    Analyze a PRD for compliance using the LangGraph workflow
    
    This endpoint takes a PRD name and description, runs the compliance analysis workflow,
    and returns detailed results including risk assessment, compliance issues, and recommendations.
    """
    try:
        if workflow is None:
            raise HTTPException(
                status_code=500, 
                detail="Workflow not initialized. Please check server logs."
            )
        
        logger.info(f"📋 Starting PRD analysis for: {request.name}")
        
        # Generate PRD content if not provided
        if not request.content:
            request.content = f"""
            Product Requirements Document
            
            Name: {request.name}
            Description: {request.description}
            
            This document outlines the requirements for {request.name}.
            {request.description}
            
            Key Features:
            - Feature 1: Basic functionality
            - Feature 2: User interface
            - Feature 3: Data processing
            
            Technical Requirements:
            - Platform: Web-based application
            - Database: Standard relational database
            - Security: User authentication and authorization
            - Performance: Response time under 2 seconds
            
            User Stories:
            - As a user, I want to access the application securely
            - As a user, I want to perform basic operations
            - As an admin, I want to manage user accounts
            
            Data Requirements:
            - User profile information
            - Application usage data
            - System logs and analytics
            """
        
        # Create PRD data for workflow
        prd_data = {
            "prd_id": f"prd_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "prd_name": request.name,
            "prd_description": request.description,
            "prd_content": request.content,
            "metadata": {
                "document_type": "product_requirements",
                "analysis_date": datetime.now().isoformat(),
                "word_count": len(request.content.split()),
                "source": "api_request"
            }
        }
        
        # Run the workflow
        logger.info(f"🚀 Running workflow for PRD: {request.name}")
        final_state = workflow.run_workflow(prd_data)
        
        # Prepare response
        response = WorkflowResponse(
            workflow_id=final_state.workflow_id,
            prd_name=final_state.prd_name,
            prd_description=final_state.prd_description,
            overall_risk_level=final_state.overall_risk_level,
            overall_confidence_score=final_state.overall_confidence_score,
            total_features_analyzed=len(final_state.extracted_features),
            critical_compliance_issues=final_state.critical_compliance_issues,
            summary_recommendations=final_state.summary_recommendations,
            non_compliant_states=final_state.non_compliant_states_dict or {},
            feature_compliance_results=final_state.feature_compliance_results or [],
            state_analysis_results=final_state.state_analysis_results or {},
            processing_time=final_state.total_processing_time
        )
        
        logger.info(f"✅ PRD analysis completed for: {request.name}")
        logger.info(f"📊 Risk Level: {final_state.overall_risk_level.upper()}")
        logger.info(f"⏱️ Processing Time: {final_state.total_processing_time:.2f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Error analyzing PRD: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze PRD: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "workflow_initialized": workflow is not None,
            "timestamp": datetime.now().isoformat(),
            "service": "LangGraph Compliance Workflow API"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LangGraph Compliance Workflow API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze_prd": "/analyze-prd",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("LANGGRAPH_HOST", "0.0.0.0")
    port = int(os.getenv("LANGGRAPH_PORT", "8000"))
    
    print("🚀 Starting LangGraph Compliance Workflow API...")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print("📚 API Documentation: http://localhost:{port}/docs")
    print("🔍 Health Check: http://localhost:{port}/health")
    print("🌐 API Base URL: http://localhost:{port}")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run(app, host=host, port=port)
