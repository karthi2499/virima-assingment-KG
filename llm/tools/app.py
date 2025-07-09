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


def read_csv_file(file_path: str):
    """Reads a CSV file and returns its content as a list of dictionaries.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        list: A list of dictionaries representing the rows in the CSV file.
    """
    print(f"Reading CSV file from path: {file_path}")
    file_path = file_path.strip()
    import pandas as pd
    try:
        df = pd.read_csv(rf'{file_path}', dtype=str, engine='pyarrow')  # Read CSV file with all data as strings
        return df.sample(20).to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        raise RuntimeError(f"Failed to read CSV file: {str(e)}")
