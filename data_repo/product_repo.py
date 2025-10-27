import datetime

from schema.pydantic_models.product import NewProductSch
from settings import PICTURE_PATH


class ProductRepo:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()

    # def get_products(self):
    #     """
    #     Returns products with attached pictures.
    #     """
    #     self._cursor.execute(
    #         """
    #     SELECT product.id, product.name, category_id, category.name as category_name, stock_quantity
    #     FROM product
    #     JOIN category ON product.category_id = category.id
    #     ORDER BY product.name
    #     """
    #     )
    #     rows = self._cursor.fetchall()
    #     products = [
    #         {
    #             "id": row[0],
    #             "name": row[1],
    #             "category": {"id": row[2], "name": row[3]},
    #             "stockQuantity": row[4],
    #             "pictures": [],
    #         }
    #         for row in rows
    #     ]
    #
    #     product_ids = [p["id"] for p in products]
    #     if not product_ids:
    #         return products
    #
    #     placeholders = ",".join("?" for _ in product_ids)
    #     self._cursor.execute(
    #         f"""
    #     SELECT pp.product_id, picture.id, picture.name, picture.path
    #     FROM product_picture pp
    #     JOIN picture ON pp.picture_id = picture.id
    #     WHERE pp.product_id IN ({placeholders})
    #     ORDER BY picture.created_at
    #     """,
    #         product_ids,
    #     )
    #     pic_rows = self._cursor.fetchall()
    #
    #     pics_by_product = {}
    #     for r in pic_rows:
    #         pid = r[0]
    #         pic = {"id": r[1], "name": r[2], "path": r[3]}
    #         pics_by_product.setdefault(pid, []).append(pic)
    #
    #     for p in products:
    #         p["pictures"] = pics_by_product.get(p["id"], [])
    #
    #     return products

    # python
    def get_products(self):
        """
        Returns products with attached pictures. Picture `path` values are converted
        to browser-accessible URLs when possible.
        """
        import os

        self._cursor.execute(
            """
        SELECT product.id, product.name, category_id, category.name as category_name, stock_quantity
        FROM product
        JOIN category ON product.category_id = category.id
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
                "pictures": [],
            }
            for row in rows
        ]

        product_ids = [p["id"] for p in products]
        if not product_ids:
            return products

        placeholders = ",".join("?" for _ in product_ids)
        self._cursor.execute(
            f"""
        SELECT pp.product_id, picture.id, picture.name, picture.path
        FROM product_picture pp
        JOIN picture ON pp.picture_id = picture.id
        WHERE pp.product_id IN ({placeholders})
        ORDER BY picture.created_at
        """,
            product_ids,
        )
        pic_rows = self._cursor.fetchall()

        pics_by_product = {}
        for r in pic_rows:
            pid = r[0]
            pic_id = r[1]
            pic_name = r[2]
            raw_path = r[3] or ""

            # convert stored path to browser-accessible URL
            if raw_path.startswith(("http://", "https://")):
                url = raw_path
            else:
                norm = raw_path.replace("\\", "/")
                filename = os.path.basename(norm) if norm else ""
                if PICTURE_PATH and PICTURE_PATH.startswith(("http://", "https://")):
                    url = PICTURE_PATH.rstrip("/") + ("/" + filename if filename else "")
                elif "resources" in norm or (PICTURE_PATH and "resources" in PICTURE_PATH):
                    # served by your blueprint at /products/pictures/<filename>
                    url = f"/api/products/pictures/{filename}" if filename else norm
                else:
                    # fallback: normalized filesystem path
                    url = norm

            pic = {"id": pic_id, "name": pic_name, "path": url}
            pics_by_product.setdefault(pid, []).append(pic)

        for p in products:
            p["pictures"] = pics_by_product.get(p["id"], [])

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

    def create_picture(self, product_id: int, picture_name: str = None, picture_url: str = None):
        # name = <product_id>_<timestamp>.jpg
        self._cursor.execute(
            """
        INSERT INTO picture (name, path)
        VALUES (?, ?)
        """,
            (picture_name, picture_url),
        )
        self._conn.commit()
        return self._cursor.lastrowid

    def attach_picture_to_product(self, product_id: int, picture_id: int):
        self._cursor.execute(
            """
        INSERT INTO product_picture (product_id, picture_id)
        VALUES (?, ?)
        """,
            (product_id, picture_id),
        )
        self._conn.commit()
