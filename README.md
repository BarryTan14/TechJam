# TechJam Project

A full-stack application combining a modern React frontend with a powerful LangGraph-powered AI backend.

## 🚀 Project Overview

TechJam is a comprehensive project that demonstrates the integration of:
- **Frontend**: Modern React application with TypeScript and Vite
- **Backend**: LangGraph-powered AI workflows with FastAPI
- **AI Integration**: LangChain and OpenAI for intelligent conversations

## 📁 Project Structure

```
TechJam/
├── frontend/           # React frontend application
│   ├── src/           # Source code
│   ├── package.json   # Frontend dependencies
│   └── README.md      # Frontend documentation
├── langgraph/         # LangGraph backend API
│   ├── main.py        # FastAPI application
│   ├── requirements.txt # Python dependencies
│   └── README.md      # Backend documentation
└── README.md          # This file
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern React with concurrent features
- **TypeScript** - Type-safe development
- **Vite** - Lightning-fast build tool
- **Modern CSS** - Beautiful, responsive design

### Backend
- **FastAPI** - High-performance async API framework
- **LangGraph** - AI workflow orchestration
- **LangChain** - LLM integration and tools
- **OpenAI** - Advanced language models

## 🚀 Quick Start

### Prerequisites

- **Node.js** (version 16 or higher)
- **Python** (version 3.8 or higher)
- **OpenAI API Key** (for AI functionality)

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:3000`

### Backend Setup

1. Navigate to the langgraph directory:
   ```bash
   cd langgraph
   ```

2. Create a virtual environment:
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

4. Create a `.env` file with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Start the backend server:
   ```bash
   python main.py
   ```

6. The API will be available at `http://localhost:8000`

## 🔗 API Integration

The frontend and backend are designed to work together seamlessly:

- **Frontend**: Runs on `http://localhost:3000`
- **Backend**: Runs on `http://localhost:8000`
- **CORS**: Configured for cross-origin requests
- **API Documentation**: Available at `http://localhost:8000/docs`

## 🎯 Features

### Frontend Features
- ⚡ **Vite** - Lightning fast development
- ⚛️ **React 18** - Latest React features
- 🔷 **TypeScript** - Type safety
- 🎨 **Modern UI** - Beautiful, responsive design
- 🔧 **ESLint** - Code quality
- 📦 **Hot Reload** - Instant updates

### Backend Features
- 🤖 **LangGraph Workflows** - Complex AI conversation flows
- 🚀 **FastAPI** - High-performance API
- 🔗 **LangChain Integration** - LLM ecosystem
- 💬 **Conversation Management** - Track conversations
- 🎯 **Sentiment Analysis** - Built-in analysis
- 📊 **Health Monitoring** - Service health checks

## 🧪 Testing the Integration

1. Start both frontend and backend servers
2. Open the frontend at `http://localhost:3000`
3. The frontend can make API calls to the backend
4. Test the chat functionality through the API

## 📚 Documentation

- **Frontend Documentation**: See `frontend/README.md`
- **Backend Documentation**: See `langgraph/README.md`
- **API Documentation**: Visit `http://localhost:8000/docs` when backend is running

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run preview      # Preview production build
```

### Backend Development
```bash
cd langgraph
python main.py       # Start development server
# or
uvicorn main:app --reload  # Start with auto-reload
```

## 🚀 Deployment

### Frontend Deployment
1. Build the frontend: `npm run build`
2. Deploy the `dist` folder to your hosting service

### Backend Deployment
1. Set up production environment variables
2. Use a production ASGI server like Gunicorn
3. Configure reverse proxy (nginx)
4. Set up monitoring and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the individual README files in `frontend/` and `langgraph/`
2. Ensure all prerequisites are installed
3. Verify environment variables are set correctly
4. Check that both servers are running on the correct ports

## 🎉 Getting Started with AI

To start using the AI features:

1. Get an OpenAI API key from [OpenAI](https://platform.openai.com/)
2. Add it to your `.env` file in the langgraph directory
3. Start the backend server
4. Test the chat endpoint at `http://localhost:8000/chat`

The LangGraph workflow will process your messages and provide intelligent responses with sentiment analysis!
