import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j Constants
neo4j_url = os.getenv("NEO4J_URL")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
neo4j_database = os.getenv("NEO4J_DATABASE")

# Gemini Constants
gemini_model_flash = os.getenv("GEMINI_MODEL_FLASH", "gemini-2.5-flash")
gemini_model_pro = os.getenv("GEMINI_MODEL_PRO", "gemini-2.5-pro")
