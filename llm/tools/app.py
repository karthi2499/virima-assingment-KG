from google.genai import types

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Neo4j Query execution function
def execute_neo4j_query(connection, query, parameters=None):
    try:
        return connection.query(query, parameters or {})
    except Exception as e:
        raise RuntimeError(f"Failed to execute Neo4j query: {str(e)}")
    

tools = [grounding_tool, execute_neo4j_query]