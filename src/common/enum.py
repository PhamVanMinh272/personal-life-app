from enum import Enum


class RoutePattern(str, Enum):
    class Products(str, Enum):
        BASE = "/api/products"
        PICTURES = "/api/products/pictures/<filename>"
        BASE_WITH_ID = "/api/products/<int:productId>"
        ATTACH_PICTURE = "/api/products/<int:productId>/attach-picture"