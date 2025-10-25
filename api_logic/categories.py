from common.db_connection import db_context_manager
from services.categories import CategoriesService


@db_context_manager
def get_all_categories(conn, **kwargs):
    categories = CategoriesService(conn).get_all_categories()
    return {"data": categories}
