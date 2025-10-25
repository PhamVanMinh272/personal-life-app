from flask import Blueprint, request

from api_logic import products

products_router = Blueprint("products", __name__)


@products_router.route("", methods=["GET"])
def get_products():
    return products.get_products()


@products_router.route("", methods=["POST"])
def create_products():
    data = request.json
    return products.create_product(**data)
