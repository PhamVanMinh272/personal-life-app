locals {
  rest_api_id = aws_api_gateway_rest_api.pl_lambda_api.id
  execution_arn = aws_api_gateway_rest_api.pl_lambda_api.execution_arn
}

resource "aws_api_gateway_rest_api" "pl_lambda_api" {
  name        = "pl_lambda_api"
  description = "API Gateway for Personal Life App"
}

resource "aws_api_gateway_resource" "api" {
  rest_api_id = local.rest_api_id
  parent_id   = aws_api_gateway_rest_api.pl_lambda_api.root_resource_id
  path_part   = "api"
}

resource "aws_api_gateway_resource" "v1" {
  rest_api_id = local.rest_api_id
  parent_id   = aws_api_gateway_resource.api.id
  path_part   = "v1"
}

resource "aws_api_gateway_resource" "categories" {
  rest_api_id = local.rest_api_id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "categories"
}

resource "aws_api_gateway_resource" "products" {
  rest_api_id = local.rest_api_id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "products"
}

resource "aws_api_gateway_resource" "swagger" {
  rest_api_id = local.rest_api_id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "swagger"
}

resource "aws_api_gateway_method" "categories_get" {
  rest_api_id   = local.rest_api_id
  resource_id   = aws_api_gateway_resource.categories.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "products_get" {
  rest_api_id   = local.rest_api_id
  resource_id   = aws_api_gateway_resource.products.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "swagger_get" {
  rest_api_id   = local.rest_api_id
  resource_id   = aws_api_gateway_resource.swagger.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "categories_lambda" {
  rest_api_id             = local.rest_api_id
  resource_id             = aws_api_gateway_resource.categories.id
  http_method             = aws_api_gateway_method.categories_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.pl_categories_function.invoke_arn
}

resource "aws_api_gateway_integration" "products_lambda" {
  rest_api_id             = local.rest_api_id
  resource_id             = aws_api_gateway_resource.products.id
  http_method             = aws_api_gateway_method.products_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.pl_products_function.invoke_arn
}

resource "aws_api_gateway_integration" "swagger_lambda" {
  rest_api_id             = local.rest_api_id
  resource_id             = aws_api_gateway_resource.swagger.id
  http_method             = aws_api_gateway_method.swagger_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.pl_swagger_function.invoke_arn
}

resource "aws_lambda_permission" "categories_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pl_categories_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${local.execution_arn}/*/*"
}

resource "aws_lambda_permission" "products_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pl_products_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${local.execution_arn}/*/*"
}

resource "aws_lambda_permission" "swagger_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pl_swagger_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${local.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "pl_api_deployment" {
  rest_api_id = local.rest_api_id

  depends_on = [
    aws_api_gateway_method.products_get,
    aws_api_gateway_integration.products_lambda,
    aws_api_gateway_method.swagger_get,
    aws_api_gateway_integration.swagger_lambda,
  ]
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.pl_api_deployment.id
  rest_api_id   = local.rest_api_id
  stage_name    = "dev"
}