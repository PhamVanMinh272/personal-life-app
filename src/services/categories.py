from src.data_repo import CategoriesRepo


class CategoriesService:
    def __init__(
        self,
        conn,
    ):
        """ """
        self._conn = conn

    def get_all_categories(self):
        return CategoriesRepo(self._conn).get_all_categories()
