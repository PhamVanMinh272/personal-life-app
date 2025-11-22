terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.81.0"
    }

  }
}
provider "aws" {
  region = var.aws_region

}

resource "aws_iam_role" "pl_lambda_role" {
    name = "pl-lambda-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "lambda.amazonaws.com"
                }
            }
        ]
    })
}

resource "aws_lambda_layer_version" "pl_layer" {
  layer_name          = "pl-layer"
  filename            = data.archive_file.pl_lambda_layer_zip.output_path
  compatible_runtimes = ["python3.11"]
  source_code_hash    = data.archive_file.pl_lambda_layer_zip.output_base64sha256
}

resource "aws_lambda_function" "pl_swagger_function" {
    function_name = "pl-swagger-function"
    role          = aws_iam_role.pl_lambda_role.arn
    handler       = "main.lambda_handler"
    runtime       = "python3.11"
    filename      = data.archive_file.swagger_lambda_zip.output_path
    source_code_hash = data.archive_file.swagger_lambda_zip.output_base64sha256
}

resource "aws_lambda_function" "pl_categories_function" {
    function_name = "pl-categories-function"
    role          = aws_iam_role.pl_lambda_role.arn
    handler       = "src.lambda_api.products.lambda_handler"
    runtime       = "python3.11"
    filename      = data.archive_file.products_lambda_zip.output_path
    source_code_hash = data.archive_file.products_lambda_zip.output_base64sha256

    layers = [aws_lambda_layer_version.pl_layer.arn]
}

resource "aws_lambda_function" "pl_products_function" {
    function_name = "pl-products-function"
    role          = aws_iam_role.pl_lambda_role.arn
    handler       = "src.lambda_api.products.lambda_handler"
    runtime       = "python3.11"
    filename      = data.archive_file.products_lambda_zip.output_path
    source_code_hash = data.archive_file.products_lambda_zip.output_base64sha256

    layers = [aws_lambda_layer_version.pl_layer.arn]
}

resource "aws_iam_role_policy_attachment" "pl_lambda_logging" {
  role       = aws_iam_role.pl_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
