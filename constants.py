import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j Constants
neo4j_url = os.getenv("NEO4J_URL", "bolt://localhost:7687")
neo4j_user = os.getenv("NEO4J_USER", "neo4j")
neo4j_password = os.getenv("NEO4J_PASSWORD", "password")
neo4j_database = os.getenv("NEO4J_DATABASE", "neo4j")

# Gemini Constants
gemini_api_key = os.getenv("GEMINI_API_KEY", "your_gemini_api_key")
gemini_model_lite = os.getenv("GEMINI_MODEL_LITE", "gemini-1.5-flash")
gemini_model_pro = os.getenv("GEMINI_MODEL_PRO", "gemini-1.5-pro")
