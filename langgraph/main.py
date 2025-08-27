from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
import json

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TechJam LangGraph API",
    description="A LangGraph-powered API for building conversational AI workflows",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    conversation_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    status: str = "success"

class WorkflowRequest(BaseModel):
    input_data: Dict[str, Any]
    workflow_type: str = "basic"

# Initialize LangChain components
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define state schema
class ConversationState:
    def __init__(self, messages: List = None, conversation_id: str = "default"):
        self.messages = messages or []
        self.conversation_id = conversation_id

# Define workflow nodes
def process_message(state: ConversationState) -> ConversationState:
    """Process the user message and generate a response"""
    if not state.messages:
        return state
    
    # Get the last user message
    last_message = state.messages[-1]
    
    # Generate response using LangChain
    response = llm.invoke([HumanMessage(content=last_message.content)])
    
    # Add AI response to state
    state.messages.append(AIMessage(content=response.content))
    
    return state

def analyze_sentiment(state: ConversationState) -> ConversationState:
    """Analyze the sentiment of the conversation"""
    if not state.messages:
        return state
    
    # Simple sentiment analysis (you can enhance this)
    last_message = state.messages[-1].content.lower()
    
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy"]
    negative_words = ["bad", "terrible", "awful", "sad", "angry", "disappointed"]
    
    sentiment = "neutral"
    if any(word in last_message for word in positive_words):
        sentiment = "positive"
    elif any(word in last_message for word in negative_words):
        sentiment = "negative"
    
    # Add sentiment analysis to state
    state.sentiment = sentiment
    return state

# Create LangGraph workflow
def create_conversation_workflow():
    """Create a LangGraph workflow for conversation processing"""
    workflow = StateGraph(ConversationState)
    
    # Add nodes
    workflow.add_node("process_message", process_message)
    workflow.add_node("analyze_sentiment", analyze_sentiment)
    
    # Define edges
    workflow.set_entry_point("process_message")
    workflow.add_edge("process_message", "analyze_sentiment")
    workflow.add_edge("analyze_sentiment", END)
    
    return workflow.compile()

# Initialize workflow
conversation_workflow = create_conversation_workflow()

# Store conversations (in production, use a database)
conversations = {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to TechJam LangGraph API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "workflow": "/workflow",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "langgraph-api"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message through the LangGraph workflow"""
    try:
        # Get or create conversation
        if request.conversation_id not in conversations:
            conversations[request.conversation_id] = []
        
        # Add user message
        conversations[request.conversation_id].append(
            HumanMessage(content=request.message)
        )
        
        # Create state
        state = ConversationState(
            messages=conversations[request.conversation_id],
            conversation_id=request.conversation_id
        )
        
        # Run workflow
        result = conversation_workflow.invoke(state)
        
        # Get the AI response
        ai_messages = [msg for msg in result.messages if isinstance(msg, AIMessage)]
        response = ai_messages[-1].content if ai_messages else "I'm sorry, I couldn't generate a response."
        
        # Update conversation
        conversations[request.conversation_id] = result.messages
        
        return ChatResponse(
            response=response,
            conversation_id=request.conversation_id,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workflow")
async def run_workflow(request: WorkflowRequest):
    """Run a custom workflow with input data"""
    try:
        # This is a placeholder for more complex workflows
        # You can extend this based on workflow_type
        result = {
            "workflow_type": request.workflow_type,
            "input_data": request.input_data,
            "output": f"Processed {request.workflow_type} workflow",
            "status": "completed"
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "type": "human" if isinstance(msg, HumanMessage) else "ai",
                "content": msg.content
            }
            for msg in conversations[conversation_id]
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
