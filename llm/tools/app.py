import json
from google.genai import types

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Neo4j Query execution function
def execute_neo4j_query(query: str):
    """Executes a Neo4j query with the given parameters.
    Args:
        query (str): The Cypher query to execute.
    Returns:
        dict: The result of the query execution.
    Raises:
        RuntimeError: If the query execution fails.
    """
    from neo4j import GraphDatabase
    from constants import neo4j_url, neo4j_user, neo4j_password
    
    connection = GraphDatabase.driver(neo4j_url, auth=(neo4j_user, neo4j_password))
    connection.verify_connectivity()  # Ensure the connection is valid
    
    if not query:
        raise ValueError("Query cannot be empty")
    
    query = query.strip()

    if query.__contains__("CREATE") or query.__contains__("DELETE") or query.__contains__("DROP"):
        raise ValueError("Query contains prohibited operations: CREATE, DELETE, or DROP")
    
    try:
        with connection.session() as session:
            result = session.execute_read(_run_and_return_query, query)
        
        response = json.dumps(result, default=str)
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to execute Neo4j query: {str(e)}")
    finally:
        connection.close()


def _run_and_return_query(tx, query):
    """
    A helper function that runs a query and fetches all results within a transaction.
    """
    result = tx.run(query)
    # Consume the result stream and return the data as a list of dictionaries.
    # This must be done within the function passed to execute_read.
    return [record.data() for record in result]
