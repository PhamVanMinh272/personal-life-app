
data "archive_file" "products_lambda_zip" {
  type = "zip"
  source_dir  = "${path.module}/../lambda_api/"
  output_path = "${path.module}/../lambda_api/products_lambda.zip"

}