from flask import Flask
from flask_cors import CORS

from src.flask_api import categories_router, products_router
from swagger.flask_main import swagger_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(swagger_bp, url_prefix="/api/swagger")
app.register_blueprint(categories_router, url_prefix="/api/categories")
app.register_blueprint(products_router, url_prefix="/api/products")


# app exit handler
@app.teardown_appcontext
def shutdown_session(exception=None):
    # should close db session here
    pass


if __name__ == "__main__":
    app.run(debug=True)
