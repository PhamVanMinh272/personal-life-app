resource "aws_api_gateway_rest_api" "pl_api_gateway" {
    name        = "pl-api-gateway"
    description = "API Gateway for PL service"
}

resource "aws_api_gateway_rest_api" "pl_lambda_api" {
  name        = "pl_lambda_api"
  description = "API Gateway for Personal Life App"
}

resource "aws_api_gateway_resource" "api" {
  rest_api_id = aws_api_gateway_rest_api.pl_lambda_api.id
  parent_id   = aws_api_gateway_rest_api.pl_lambda_api.root_resource_id
  path_part   = "api"
}

resource "aws_api_gateway_resource" "v1" {
  rest_api_id = aws_api_gateway_rest_api.pl_lambda_api.id
  parent_id   = aws_api_gateway_resource.api.id
  path_part   = "v1"
}

resource "aws_api_gateway_resource" "products" {
  rest_api_id = aws_api_gateway_rest_api.pl_lambda_api.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "products"
}

resource "aws_api_gateway_resource" "swagger" {
  rest_api_id = aws_api_gateway_rest_api.pl_lambda_api.id
  parent_id   = aws_api_gateway_resource.v1.id
  path_part   = "swagger"
}

resource "aws_api_gateway_method" "pl_products_lambda_method" {
  rest_api_id   = aws_api_gateway_rest_api.pl_lambda_api.id
  resource_id   = aws_api_gateway_resource.products.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "pl_swagger_lambda_method" {
  rest_api_id   = aws_api_gateway_rest_api.pl_lambda_api.id
  resource_id   = aws_api_gateway_resource.swagger.id
  http_method   = "GET"
  authorization = "NONE"
}


resource "aws_lambda_permission" "pl_api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pl_products_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.pl_lambda_api.execution_arn}/*/*"
}

resource "aws_api_gateway_integration" "pl_products_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.pl_lambda_api.id
  resource_id             = aws_api_gateway_resource.products.id
  http_method             = aws_api_gateway_method.pl_products_lambda_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.pl_products_function.invoke_arn
}

resource "aws_lambda_permission" "pl_swagger_api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pl_swagger_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.pl_lambda_api.execution_arn}/*/*"
}

resource "aws_api_gateway_integration" "pl_swagger_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.pl_lambda_api.id
  resource_id             = aws_api_gateway_resource.swagger.id
  http_method             = aws_api_gateway_method.pl_swagger_lambda_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.pl_swagger_function.invoke_arn
}

