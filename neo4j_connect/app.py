from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, url, user, password):
        self.driver = GraphDatabase.driver(url, auth=(user, password))

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
