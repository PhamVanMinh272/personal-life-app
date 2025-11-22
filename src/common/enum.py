from enum import Enum


class RoutePattern:
    class Products(str, Enum):
        BASE = "/api/v1/products"
        PICTURES = "/api/v1/products/pictures/<filename>"
        BASE_WITH_ID = "/api/v1/products/<int:productId>"
        ATTACH_PICTURE = "/api/v1/products/<int:productId>/attach-picture"

    class Categories(str, Enum):
        BASE = "/api/v1/categories"
        BASE_WITH_ID = "/api/v1/categories/<int:categoryId>"