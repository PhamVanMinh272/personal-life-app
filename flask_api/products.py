import os

from flask import Blueprint, request, jsonify, send_from_directory

from api_logic import products

products_router = Blueprint("products", __name__)


@products_router.route("", methods=["GET"])
def get_products():
    return products.get_products()


@products_router.route("", methods=["POST"])
def create_products():
    data = request.json
    return products.create_product(**data)


@products_router.route("/<int:productId>/attach-picture", methods=["POST"])
def attach_picture_to_product(productId):
    picture_file = request.files.get("pictureFile")
    if not picture_file:
        return jsonify({"error": "pictureFile is required"}), 400

    try:
        picture_data = picture_file.read()
    except Exception as e:
        return jsonify({"error": "failed to read uploaded file", "details": str(e)}), 500

    result = products.attach_picture_to_product(productId=productId, pictureData=picture_data)

    # normalize and return JSON so Swagger can display response
    if isinstance(result, dict):
        return jsonify(result), 200
    if result is True:
        return jsonify({"success": True, "productId": productId}), 200
    if result is False or result is None:
        return jsonify({"success": False}), 400

    return jsonify({"result": result}), 200



@products_router.route("/pictures/<path:filename>", methods=["GET"])
def serve_product_picture(filename):
    """
    Serve files saved under `resources/pictures`.
    Access URL: `/products/pictures/<filename>` (assuming blueprint mounted at `/products`).
    """
    return send_from_directory(os.path.join("resources", "pictures"), filename)
