import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ENV = os.environ.get("ENV", "local")

# DB
SQLITE_PATH = "/mnt/efs/personal_life.db"
DDL_PATH = os.path.join("/var/task", "resources", "ddl.sql")
DML_PATH = os.path.join("/var/task", "resources", "dml.sql")
if ENV == "local":
    if not os.path.exists(SQLITE_PATH):
        logger.info("Running in Flask local environment")
        SQLITE_PATH = "resources/personal_life.db"
        DDL_PATH = os.path.join("resources", "ddl.sql")
        DML_PATH = os.path.join("resources", "dml.sql")
        PICTURE_PATH = os.path.join("resources", "pictures")

    if not os.path.exists(SQLITE_PATH):
        # to init db in local env, please comment this block
        # # run aws lambda in local
        logger.info("Running in lambda local environment")
        SQLITE_PATH = os.path.join(os.pardir, "resources", "personal_life.db")
        DDL_PATH = os.path.join(os.pardir, "resources", "ddl.sql")
        DML_PATH = os.path.join(os.pardir, "resources", "dml.sql")
        PICTURE_PATH = "personal_life_app/pictures"  # s3
