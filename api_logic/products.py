from common.db_connection import db_context_manager
from schema.pydantic_models.product import NewProductSch
from services.products import ProductService


@db_context_manager
def get_products(conn, **kwargs):
    products = ProductService(conn).get_products()
    return {"data": products}


@db_context_manager
def create_product(conn, **kwargs):
    product_data = NewProductSch(**kwargs)
    product_id = ProductService(conn).create_product(product_data)
    return {"data": {"productId": product_id}}
