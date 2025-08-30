# RAG Implementation for PRD Parser Agent

## Overview

This document describes the Retrieval Augmented Generation (RAG) feature implemented in the PRD Parser Agent. The RAG system enhances the agent's ability to parse PRD documents by providing relevant terminology context from a MongoDB database.

## Architecture

### Components

1. **MongoDB Database**: Stores terminology terms and descriptions
2. **PRD Parser Agent**: Enhanced with RAG capabilities
3. **Term Extraction Engine**: Identifies potential terms in PRD content
4. **RAG Augmentation Module**: Enhances prompts with relevant context

### Database Schema

```json
{
  "_id": ObjectId("..."),
  "term": "CDS",
  "description": "Compliance Detection System"
}
```

## Implementation Details

### 1. MongoDB Connection

```python
def _initialize_mongodb(self):
    """Initialize MongoDB connection"""
    try:
        self.mongo_client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=SERVER_SELECTION_TIMEOUT_MS,
            connectTimeoutMS=CONNECTION_TIMEOUT_MS
        )
        db = self.mongo_client[DATABASE_NAME]
        self.collection = db[COLLECTION_NAME]
        # Test connection
        self.mongo_client.admin.command('ping')
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        self.mongo_client = None
        self.collection = None
```

### 2. RAG Retrieval with Cursor

```python
def _retrieve_relevant_terms(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """Retrieve relevant terms from MongoDB using RAG capabilities"""
    if not self.collection:
        return []
    
    try:
        # Create cursor for keyword search
        cursor: Cursor = self.collection.find(
            {"term": {"$regex": query, "$options": "i"}}
        ).limit(max_results)
        
        # Convert cursor to list
        results = list(cursor)
        
        # If no exact matches, try broader search
        if not results:
            cursor: Cursor = self.collection.find({
                "$or": [
                    {"term": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}}
                ]
            }).limit(max_results)
            results = list(cursor)
        
        return results
        
    except Exception as e:
        print(f"⚠️ Error retrieving terms from MongoDB: {e}")
        return []
```

### 3. Term Extraction from Content

```python
def _extract_potential_terms(self, content: str) -> List[str]:
    """Extract potential terms from PRD content for RAG lookup"""
    import re
    
    # Extract acronyms (2-4 capital letters)
    acronyms = re.findall(r'\b[A-Z]{2,4}\b', content)
    
    # Extract potential feature names (capitalized words)
    feature_names = re.findall(r'\b[A-Z][a-zA-Z]*(?:[A-Z][a-zA-Z]*)*\b', content)
    
    # Extract technical terms
    technical_terms = re.findall(r'\b(?:API|SDK|UI|UX|DB|ML|AI|CDN|SLA|GDPR|CCPA|BIPA|HIPAA|PII)\b', content, re.IGNORECASE)
    
    # Combine and deduplicate
    all_terms = acronyms + feature_names + technical_terms
    unique_terms = list(set(all_terms))
    
    # Filter out common words
    common_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'MAN', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'ITS', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 'USE'}
    filtered_terms = [term for term in unique_terms if term.upper() not in common_words and len(term) > 1]
    
    return filtered_terms[:10]  # Limit to top 10 terms
```

### 4. Prompt Augmentation

```python
def _augment_prompt_with_rag(self, base_prompt: str, prd_content: str) -> str:
    """Augment the prompt with relevant terminology from RAG"""
    # Extract potential terms from PRD content
    potential_terms = self._extract_potential_terms(prd_content)
    
    # Retrieve relevant terms from MongoDB
    relevant_terms = []
    for term in potential_terms:
        retrieved_terms = self._retrieve_relevant_terms(term)
        relevant_terms.extend(retrieved_terms)
    
    # Remove duplicates and limit to top 3
    unique_terms = []
    seen_terms = set()
    for term_doc in relevant_terms:
        if term_doc['term'] not in seen_terms and len(unique_terms) < 3:
            unique_terms.append(term_doc)
            seen_terms.add(term_doc['term'])
    
    # If no relevant terms found, return original prompt
    if not unique_terms:
        return base_prompt + "\n\nNote: No relevant terminology found in database."
    
    # Augment prompt with RAG context
    rag_context = "\n\nRELEVANT TERMINOLOGY FROM DATABASE:\n"
    for term_doc in unique_terms:
        rag_context += f"- {term_doc['term']}: {term_doc['description']}\n"
    
    rag_context += "\nUse this terminology context to enhance your analysis and ensure consistency with established terms."
    
    return base_prompt + rag_context
```

## Usage Examples

### 1. Basic RAG Search

```python
from agents import PRDParserAgent

# Create agent
agent = PRDParserAgent(llm=None)

# Search for terminology
results = agent.search_terminology("CDS", max_results=3)
for result in results:
    print(f"{result['term']}: {result['description']}")
```

### 2. Full PRD Parsing with RAG

```python
# Parse PRD with RAG augmentation
result = agent.parse_prd(
    prd_name="Compliance System PRD",
    prd_description="A system for compliance detection",
    prd_content="This PRD describes a CDS that uses GH for routing..."
)

print(f"Agent: {result.agent_name}")
print(f"RAG enabled: {result.input_data.get('rag_enabled', False)}")
print(f"Thought process: {result.thought_process}")
```

### 3. Get All Terminology

```python
# Retrieve all terminology from database
all_terms = agent.get_all_terminology()
for term in all_terms:
    print(f"{term['term']}: {term['description']}")
```

## RAG Workflow

### 1. Content Analysis
- Extract potential terms from PRD content using regex patterns
- Identify acronyms, feature names, and technical terms
- Filter out common words and limit results

### 2. Database Query
- Use MongoDB cursor for efficient querying
- Search for exact term matches first
- Fall back to broader search in descriptions
- Limit results to top 3 most relevant terms

### 3. Context Augmentation
- Retrieve relevant terminology from database
- Remove duplicates and prioritize unique terms
- Augment the base prompt with RAG context
- Provide clear instructions for using the context

### 4. Enhanced Parsing
- Use augmented prompt for LLM processing
- Maintain fallback mechanisms for robustness
- Include RAG context in analysis results

## Error Handling

### MongoDB Connection Failures
- Graceful degradation when MongoDB is unavailable
- Fallback to standard parsing without RAG
- Clear error messages for debugging

### Query Failures
- Exception handling for database queries
- Empty result sets when no matches found
- Logging of errors for monitoring

### Content Processing
- Robust term extraction with multiple patterns
- Handling of edge cases in content parsing
- Validation of extracted terms

## Performance Considerations

### Database Optimization
- Use indexes on term and description fields
- Limit query results to prevent memory issues
- Connection pooling for efficient resource usage

### Caching Strategy
- Consider caching frequently accessed terms
- Implement connection reuse for multiple queries
- Optimize cursor usage for large result sets

### Memory Management
- Limit extracted terms to prevent memory bloat
- Clean up database connections properly
- Use generators for large result sets

## Testing

### Unit Tests
- MongoDB connection testing
- Term extraction validation
- RAG augmentation verification
- Error handling scenarios

### Integration Tests
- Full PRD parsing with RAG
- Database query performance
- End-to-end workflow validation

### Test Script
Run the test script to verify RAG functionality:

```bash
cd langgraph
python test_rag_prd_parser.py
```

## Configuration

### MongoDB Settings
Update `mongodb_config.py` for your environment:

```python
MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
DATABASE_NAME = "TechJam"
COLLECTION_NAME = "terminology"
CONNECTION_TIMEOUT_MS = 5000
SERVER_SELECTION_TIMEOUT_MS = 5000
```

### Agent Configuration
The PRD Parser Agent automatically initializes RAG capabilities:

```python
agent = PRDParserAgent(llm=your_llm_instance)
# RAG is automatically enabled if MongoDB connection succeeds
```

## Benefits

### Enhanced Accuracy
- Consistent terminology usage across analyses
- Context-aware feature extraction
- Improved understanding of domain-specific terms

### Scalability
- Centralized terminology management
- Easy addition of new terms
- Efficient querying with MongoDB cursors

### Maintainability
- Clear separation of concerns
- Robust error handling
- Comprehensive testing coverage

## Future Enhancements

### Semantic Search
- Implement vector embeddings for semantic similarity
- Use MongoDB Atlas vector search capabilities
- Enhanced relevance scoring

### Dynamic Learning
- Update terminology based on usage patterns
- Learn new terms from PRD content
- Adaptive relevance algorithms

### Advanced Filtering
- Category-based term filtering
- Context-aware relevance scoring
- Multi-language support

## Conclusion

The RAG implementation significantly enhances the PRD Parser Agent's capabilities by providing relevant terminology context from a MongoDB database. The system is robust, scalable, and maintains high performance while ensuring accurate and consistent feature extraction from PRD documents.
