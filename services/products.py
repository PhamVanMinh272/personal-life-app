from data_repo.product_repo import ProductRepo
from schema.pydantic_models.product import NewProductSch


class ProductService:
    def __init__(self, conn):
        self._conn = conn

    def get_products(self):
        return ProductRepo(self._conn).get_products()

    def create_product(self, new_product: NewProductSch):
        return ProductRepo(self._conn).create_product(new_product)
