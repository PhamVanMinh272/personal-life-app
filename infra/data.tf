
data "archive_file" "swagger_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../swagger"
  output_path = "${path.module}/../swagger_lambda.zip"
}

data "archive_file" "products_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/.."
  output_path = "${path.module}/../products_lambda.zip"

  excludes = [
    "**/__pycache__/**",
    "**/*.pyc",
    ".venv/**",
    "src/services/u2net/u2net.pth",
    "*.zip",
    "infra/**",
    "tests/**",
    ".gitignore",
    ".git/**",
    "README.md",
    "LICENSE",
    "requirements.txt",
    ".idea/**",
    "src/flask_api/**",
  ]
}

data "archive_file" "pl_lambda_layer_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../layer/python_standard"
  output_path = "${path.module}/../layer/python.zip"
}

