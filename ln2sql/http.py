import mysql.connector
import os

from flask import Flask, request, jsonify
from .ln2sql import Ln2sql
from urllib.parse import unquote

app = Flask(__name__)

connection = mysql.connector.connect(
    host='0.0.0.0',
    user='root',
    password='password',
    database='ln2sql',
)

@app.route('/api/query', methods=['POST'])
def query():
    k = unquote(request.args.get('key'))

    if k is None or k=="" :
        return jsonify({'error': 'key is required'})

    if k != os.getenv("API_KEY") :
        return jsonify({'error': 'wrong api key'})

    query = request.get_data(False, True)

    sql = Ln2sql(
        database_path="database_store/city.sql",
        language_path="lang_store/ukrainian.csv",
        json_output_path=None,
        thesaurus_path=None,
        stopwords_path=None,
    ).get_query(query)

    cursor = connection.cursor()
    cursor.execute(sql)

    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]

    # Convert the result to a list of dictionaries
    resp = []
    for row in rows:
        resp.append(dict(zip(columns, row)))

    return jsonify({'data': resp})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)