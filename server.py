import json

from flask import Flask

from database import DocumentDB
from index import SearchIndex
from parser import parse_query

db = DocumentDB()
recipes = db.list()
search_index = SearchIndex(recipes)

app = Flask(__name__)


@app.route("/api/v1/search/<query>")
def search(query):
    try:
        query_tree = parse_query(query)
    except Exception as err:
        return json.dumps({'error': f"Incorrect syntax: {err}"}), 400

    results = search_index.search(query_tree)
    return json.dumps({'results': results}, default=lambda obj: obj.__dict__)

if __name__ == '__main__':
    app.run()
