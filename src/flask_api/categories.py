from flask import Blueprint

from src.api_logic import categories

categories_router = Blueprint("categories", __name__)


@categories_router.route("", methods=["GET"])
def get_all_categories():
    return categories.get_all_categories()
