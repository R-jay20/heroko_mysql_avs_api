from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection details
db_config = {
    "host": "gator3041.hostgator.com",
    "user": "norsamel_amoecvotingsystem",
    "port": "3306",
    "password": "pFtD@iI0fpn^",
    "database": "norsamel_amoec_voting_system"
}


# Helper function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
    return None

# Select endpoint
@app.route('/select', methods=['GET'])
def select_data():
    query = request.args.get('query')  # Get query from request
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if connection and connection.is_connected():
            connection.close()

# Insert endpoint
@app.route('/insert', methods=['POST'])
def insert_data():
    table = request.json.get('table')  # e.g., "tbl_schedule"
    data = request.json.get('data')   # e.g., {"column1": "value1", "column2": "value2"}
    
    if not table or not data:
        return jsonify({"error": "Table and data must be provided"}), 400

    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        columns = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        cursor.execute(query, list(data.values()))
        connection.commit()
        return jsonify({"message": "Record inserted", "id": cursor.lastrowid})
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if connection and connection.is_connected():
            connection.close()

# Delete endpoint
@app.route('/delete', methods=['DELETE'])
def delete_data():
    table = request.json.get('table')  # e.g., "tbl_schedule"
    condition = request.json.get('condition')  # e.g., "id = 1"

    if not table or not condition:
        return jsonify({"error": "Table and condition must be provided"}), 400

    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query)
        connection.commit()
        return jsonify({"message": f"{cursor.rowcount} record(s) deleted"})
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1000)

