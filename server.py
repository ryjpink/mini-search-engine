import json

from flask import Flask, request

from database import DocumentDB
from index import SearchIndex
from parser import parse_query

db = DocumentDB()
recipes = db.list()
search_index = SearchIndex(recipes)

app = Flask(__name__)


@app.route("/api/v1/search")
def search():
    try:
        query_text = request.args.get('q')
        query = parse_query(query_text)
    except Exception as err:
        return json.dumps({'error': f"Incorrect syntax: {err}"}), 400

    results = search_index.search(query)
    return json.dumps({'results': results}, default=lambda obj: obj.__dict__)

if __name__ == '__main__':
    app.run()
