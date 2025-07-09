# Virima Assignment - Knowledge Graph (KG)

This project is a Flask-based API for interacting with a Neo4j knowledge graph, enhanced with Google Gemini LLM integration for natural language queries and data operations. It supports CSV data ingestion, Cypher query execution, and schema discovery, with a focus on ease of use and extensibility.

## Features
- **REST API** for querying and managing a Neo4j database
- **Google Gemini LLM** integration for natural language chat and Cypher query generation
- **CSV data ingestion** with duplicate and null handling
- **Schema discovery** for Neo4j nodes and relationships
- **CORS support** for cross-origin requests

## Project Structure
```
app.py                  # Main Flask app entry point
constants.py            # Environment and configuration constants
requirements.txt        # Python dependencies
llm/                    # LLM integration and tools
  app.py                # LLM interface and chat logic
  system-prompt.txt     # System prompt for LLM
  tools/app.py          # LLM tools (Google Search, Neo4j, CSV)
neo4j_connect/          # Neo4j connection and schema logic
  app.py                # Neo4j connection class
  queries.json          # Cypher queries for schema extraction
dataset/                # Example CSV datasets
```

## Setup
1. **Clone the repository**
2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure environment variables**:
   - Create a `.env` file in the root directory with the following:
     ```env
     NEO4J_URL=bolt://localhost:7687
     NEO4J_USER=neo4j
     NEO4J_PASSWORD=your_password
     NEO4J_DATABASE=neo4j
     GEMINI_MODEL_FLASH=gemini-2.5-flash
     GEMINI_MODEL_PRO=gemini-2.5-pro
     ```
4. **Run the application**:
   ```powershell
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

## API Endpoints
- `GET /health` — Check Neo4j connection health
- `POST /chat` — Chat with Gemini LLM (natural language to Cypher)
- `POST /query` — Execute a Cypher query
- `GET /schema` — Get Neo4j schema summary
- `POST /load_data` — Load data using a Cypher query (e.g., `LOAD CSV`)

## LLM System Prompt
The LLM is instructed to:
- Answer Neo4j/OpenCypher questions with Cypher queries and JSON responses
- Summarize queries and results in plain language
- Generate `LOAD CSV` queries for file ingestion, handling duplicates and nulls

## Example Usage
**Chat with LLM:**
```json
POST /chat
{
  "message": "Show me all movies released after 2010",
  "mode": "neo4j_chat",
  "model": "flash"
}
```

**Load CSV Data:**
```json
POST /load_data
{
  "query": "LOAD CSV WITH HEADERS FROM 'file:///dataset/movies.csv' AS row ..."
}
```

## Notes
- Ensure Neo4j is running and accessible at the configured URL.
- The LLM uses Google Gemini via the `google-genai` package.
- For CSV ingestion, the system handles duplicates and nulls as per the system prompt.

## License
This project is for educational and demonstration purposes.
