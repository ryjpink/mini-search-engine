import json

from flask import Flask, request

from database import DocumentDB
from index import SearchIndex
from parser import parse_query

RESULTS_PER_PAGE: int = 10

db = DocumentDB()
recipes = db.list()
search_index = SearchIndex(recipes)

app = Flask(__name__)


@app.route("/api/v1/search")
def search():
    try:
        query_text = request.args.get('q', type=str)
        query = parse_query(query_text)
    except Exception as err:
        return json.dumps({'error': f"Incorrect syntax: {err}"}), 400

    start = request.args.get('start', type=int, default=0)
    limit = start + RESULTS_PER_PAGE + 1
    results = search_index.search(query, start=start, limit=limit)
    has_more = len(results) > RESULTS_PER_PAGE
    return json.dumps(
        {'results': results[:RESULTS_PER_PAGE], 'more': has_more},
        default=lambda obj: obj.__dict__)

if __name__ == '__main__':
    app.run()
