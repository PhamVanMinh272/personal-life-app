from schema.pydantic_models.product import NewProductSch


class ProductRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    def get_products(self):
        self._cursor.execute(
            """
        SELECT product.id, product.name, category_id, category.name as category_name, stock_quantity 
        FROM product
        join category on product.category_id = category.id
        ORDER BY product.name
        """
        )
        rows = self._cursor.fetchall()
        products = [
            {
                "id": row[0],
                "name": row[1],
                "category": {"id": row[2], "name": row[3]},
                "stockQuantity": row[4],
            }
            for row in rows
        ]
        return products

    def create_product(self, new_product: NewProductSch):

        self._cursor.execute(
            """
        INSERT INTO product (name, category_id, stock_quantity)
        VALUES (?, ?, ?)
        """,
            (new_product.name, new_product.category_id, new_product.stock_quantity),
        )
        self._conn.commit()
        return self._cursor.lastrowid
