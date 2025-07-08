import constants as const
from flask_cors import CORS
from flask import Flask, request, jsonify
from neo4j_connect.app import Neo4jConnection

# Flask application setup
app = Flask(__name__)
CORS(app)

# Initialize Neo4j connection
neo4j_conn = Neo4jConnection(const.neo4j_url, const.neo4j_user, const.neo4j_password)


@app.route('/health', methods=['GET'])
def health_check():
    health_status = neo4j_conn.check_health()
    return jsonify(health_status), 200 if health_status['status'] == 'ok' else 500


@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid input"}), 400
    return jsonify({"message": data['message']}), 200


@app.route('/query', methods=['POST'])
def execute_query():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid input"}), 400

    query = data['query']
    parameters = data.get('parameters', {})

    try:
        result = neo4j_conn.query(query, parameters)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.teardown_appcontext
def close_neo4j_connection(error):
    if hasattr(neo4j_conn, 'close'):
        neo4j_conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
