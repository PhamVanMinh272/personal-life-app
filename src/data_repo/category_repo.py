class CategoriesRepo:

    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_all_categories(self) -> list[dict]:
        self._cursor.execute(
            """
            SELECT category.id, name
            FROM category"""
        )
        rows = self._cursor.fetchall()
        sections = [
            {
                "id": row[0],
                "name": row[1],
            }
            for row in rows
        ]
        return sections
