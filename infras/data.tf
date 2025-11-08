data "archive_file" "products_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/../src/products_lambda.zip"

  excludes = [
    "**/__pycache__/**",
    "**/*.pyc",
    ".venv/**",
    "services/u2net/u2net.pth",
    "*.zip"
  ]
}