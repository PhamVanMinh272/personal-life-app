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


@db_context_manager
def attach_picture_to_product(conn, **kwargs):
    product_id = kwargs.get("productId")
    picture_data = kwargs.get("pictureData")
    picture_id, picture_url = ProductService(conn).attach_picture_to_product(
        product_id, picture_data
    )
    return {"data": {"pictureId": picture_id, "pictureUrl": picture_url}}
