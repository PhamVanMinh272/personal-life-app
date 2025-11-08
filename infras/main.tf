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

resource "aws_api_gateway_rest_api" "pl_api_gateway" {
    name        = "pl-api-gateway"
    description = "API Gateway for PL service"
}

resource "aws_lambda_function" "pl_products_function" {
    function_name = "pl-products-function"
    role          = aws_iam_role.pl_lambda_role.arn
    handler       = "lambda_api.products.lambda_handler"
    runtime       = "python3.11"
    filename      = data.archive_file.products_lambda_zip.output_path
    source_code_hash = data.archive_file.products_lambda_zip.output_base64sha256
}