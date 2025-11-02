import json


def lambda_handler(event, context):
    # Sample product data
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Smartphone", "price": 499.99},
        {"id": 3, "name": "Tablet", "price": 299.99},
    ]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(products)
    }