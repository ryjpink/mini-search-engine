from database import DocumentDB
from index import SearchIndex
from parser import parse_query


def main():
    db = DocumentDB()
    recipes = db.list()
    search_index = SearchIndex(recipes)
    while True:
        text = input("Enter the ingredients you have: ")
        try:
            query = parse_query(text)
        except Exception as err:
            print(f"Incorrect syntax: {err}")
            continue
        results = search_index.search(query)
        print(f"Showing results for: {query}")
        if len(results) == 0:
            print("No matching recipes found")
        else:
            print("You could make:")
            for result in results:
                print(f"- {result}")


if __name__ == '__main__':
    main()
