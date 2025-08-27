# TechJam LangGraph Backend

A powerful LangGraph-powered API for building conversational AI workflows using FastAPI and LangChain.

## Features

- 🤖 **LangGraph Workflows** - Build complex AI conversation flows
- 🚀 **FastAPI** - High-performance async API framework
- 🔗 **LangChain Integration** - Seamless integration with LangChain ecosystem
- 💬 **Conversation Management** - Track and manage conversation history
- 🎯 **Sentiment Analysis** - Built-in sentiment analysis capabilities
- 🔒 **CORS Support** - Ready for frontend integration
- 📊 **Health Monitoring** - Built-in health check endpoints

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LLM functionality)
- pip (Python package manager)

## Installation

1. Navigate to the langgraph directory:
   ```bash
   cd langgraph
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the langgraph directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Base URL: `http://localhost:8000`

#### GET `/`
- **Description**: Root endpoint with API information
- **Response**: API welcome message and available endpoints

#### GET `/health`
- **Description**: Health check endpoint
- **Response**: Service health status

#### POST `/chat`
- **Description**: Process chat messages through LangGraph workflow
- **Request Body**:
  ```json
  {
    "message": "Hello, how are you?",
    "conversation_id": "user123"
  }
  ```
- **Response**:
  ```json
  {
    "response": "I'm doing well, thank you for asking!",
    "conversation_id": "user123",
    "status": "success"
  }
  ```

#### POST `/workflow`
- **Description**: Run custom workflows
- **Request Body**:
  ```json
  {
    "input_data": {"key": "value"},
    "workflow_type": "basic"
  }
  ```

#### GET `/conversations/{conversation_id}`
- **Description**: Get conversation history
- **Response**: List of messages in the conversation

## API Documentation

Once the server is running, you can access:

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## LangGraph Workflow

The application includes a sample LangGraph workflow with two nodes:

1. **process_message**: Processes user input and generates AI responses
2. **analyze_sentiment**: Analyzes the sentiment of the conversation

### Workflow Flow:
```
User Input → process_message → analyze_sentiment → Response
```

## Project Structure

```
langgraph/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env               # Environment variables (create this)
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for LLM functionality)

### Customization

You can customize the LangGraph workflow by:

1. Adding new nodes to the workflow
2. Modifying the state schema
3. Creating new workflow types
4. Adding more sophisticated sentiment analysis

## Development

### Adding New Workflow Nodes

```python
def my_custom_node(state: ConversationState) -> ConversationState:
    # Your custom logic here
    return state

# Add to workflow
workflow.add_node("my_custom_node", my_custom_node)
```

### Extending the State

```python
class ConversationState:
    def __init__(self, messages: List = None, conversation_id: str = "default", custom_field: str = None):
        self.messages = messages or []
        self.conversation_id = conversation_id
        self.custom_field = custom_field
```

## Error Handling

The API includes comprehensive error handling:

- HTTP 404: Resource not found
- HTTP 500: Internal server error
- Proper error messages and status codes

## CORS Configuration

The API is configured to allow requests from `http://localhost:3000` (frontend). You can modify the CORS settings in `main.py` if needed.

## Production Deployment

For production deployment:

1. Use a production ASGI server like Gunicorn
2. Set up proper environment variables
3. Configure a reverse proxy (nginx)
4. Set up monitoring and logging
5. Use a database for conversation storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
