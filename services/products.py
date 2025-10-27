import datetime
from pathlib import Path

from data_repo.product_repo import ProductRepo
from schema.pydantic_models.product import NewProductSch
from common.s3_client import S3Client
from settings import ENV


class ProductService:
    def __init__(self, conn):
        self._conn = conn

    def get_products(self):
        return ProductRepo(self._conn).get_products()

    def create_product(self, new_product: NewProductSch):
        return ProductRepo(self._conn).create_product(new_product)


    def attach_picture_to_product(self, product_id: int, picture_data: bytes):
        """
        Save picture to `resources/pictures` when ENV == 'local', otherwise upload to S3.
        Returns (picture_id, picture_url).
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        picture_name = f"product_{product_id}_{timestamp}.jpg"

        if ENV == "local":
            pictures_dir = Path("resources") / "pictures"
            pictures_dir.mkdir(parents=True, exist_ok=True)
            file_path = pictures_dir / picture_name
            with file_path.open("wb") as f:
                f.write(picture_data)
            picture_url = str(file_path)
        else:
            s3_client = S3Client()
            picture_url = s3_client.put_object_content(picture_name, picture_data)

        repo = ProductRepo(self._conn)
        picture_id = repo.create_picture(product_id, picture_name, picture_url)
        repo.attach_picture_to_product(product_id, picture_id)
        return picture_id, picture_url