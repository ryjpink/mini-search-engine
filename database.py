import sqlite3
from typing import List

from document import Document

class DocumentDB:
    def __init__(self, file_name='index.db'):
        self.c = sqlite3.connect(file_name)
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS documents(
                dish_name TEXT PRIMARY KEY,
                ingredients TEXT)
        """)

    def add(self, doc: Document):
        self.c.execute("""
            INSERT OR FAIL INTO documents (dish_name, ingredients)
            VALUES (:dish_name, :ingredients)""",
            {
                "dish_name": doc.dish,
                "ingredients": doc.body
            })
        self.c.commit()

    def list(self) -> List[Document]:
        result = []
        for dish_name, ingredients in self.c.execute("SELECT dish_name, ingredients FROM documents"):
            item = Document(dish_name, ingredients)
            result.append(item)
        return result


def populate_test_data():
    db = DocumentDB()
    recipes = [
        Document("random dessert", "salt egg caramel butter"),
        Document("meatfloss bun", "flour meatfloss mayonnaise water egg"),
        Document("bacon stir fry cabbage", "bacon cabbage garlic"),
        Document("kimchi tofu stew", "tofu kimchi cabbage"),
        Document("taro spread", "taro flour sugar water salt milk butter")
    ]
    for doc in recipes:
        db.add(doc)


if __name__ == "__main__":
    populate_test_data()



