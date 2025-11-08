import json

from src.settings import logger
from src.api_logic import products
from src.common.api_utils import exception_handler
from src.common.enum import RoutePattern


@exception_handler
def lambda_handler(event, context):
    """
    AWS Lambda handler for product-related API requests.
    """
    get_paths = {
        RoutePattern.Products.BASE.value: products.get_products,
    }
    post_paths = {
        RoutePattern.Products.BASE: products.create_product,
        RoutePattern.Products.ATTACH_PICTURE: products.attach_picture_to_product,
    }
    path = event.get("path", "")
    logger.info(f"Path: {path}")
    method = event.get("httpMethod", "GET")
    body = json.loads(event.get("body", "{}") or "{}")
    if method == "GET":
        paths = get_paths
    elif method == "POST":
        paths = post_paths
    else:
        raise Exception("Method Not Allowed")
    if path in paths:
        function_name = paths[path]
        result = function_name(**body)
    else:
        raise Exception("Not found")



    return result


if __name__ == "__main__":
    # Test event
    test_event = {
        "path": "/api/v1/products",
        "httpMethod": "GET",
        "headers": {},
        "queryStringParameters": {},
        "body": None,
        "isBase64Encoded": False,
    }
    rs = lambda_handler(test_event, None)
    body_json = json.loads(rs["body"])
    print(json.dumps(body_json, indent=4, ensure_ascii=False))
