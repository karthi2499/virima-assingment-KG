import json
from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, url, user, password):
        self.driver = GraphDatabase.driver(url, auth=(user, password))
        self.schema = self.get_schema()

    def close(self):
        self.driver.close()

    def check_health(self):
        with self.driver.session() as session:
            try:
                session.run("RETURN 1")
                return {"status": "ok"}
            except Exception as e:
                return {"status": "error", "message": str(e)}

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
        
    def get_schema(self):
        
        with open("neo4j_connect/queries.json", "r") as file:
            queries = json.load(file)

        with self.driver.session() as session:
            result = session.run(queries["node_property_query"])
            node_props = [record.data() for record in result]

            result = session.run(queries["edge_property_query"])
            rel_props = [record.data() for record in result]

            result = session.run(queries["node_edge_relationship_query"])
            rels = [record.data() for record in result]

        node_properties = ""
        for node in node_props:
            output = node["output"]
            node_properties += f"- (:`{output['labels']}`): {output['properties']}\n"

        edge_properties = ""
        for edge in rel_props:
            output = edge["output"]
            edge_properties += f"- [:`{output['type']}`]: {output['properties']}\n"

        relationships = ""
        for rel in rels:
            output = rel["output"]
            relationships += f"(:`{output['source']}`) - [:`{output['relationship']}`] -> (:`{output['target'][-1]}`)\n"
        
        schema = f"""
This is the schema representation of the Neo4j database.
Node properties are the following:
{node_properties}
Relationship properties are the following:
{edge_properties}
Relationship point from source to target nodes
{relationships}
Make sure to respect relationship types and directions
"""
        return schema.strip()
