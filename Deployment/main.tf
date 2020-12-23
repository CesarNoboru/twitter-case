terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}
provider "aws" {
  region = var.region
}

resource "aws_iam_role" "apigw" {
  name = "twitter-case-role-apigw"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "apigateway.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy" "apigw" {
  name = "apigw-role-policy"
  role = aws_iam_role.apigw.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:GetLogEvents",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_role" "role_lambda" {
  name = "twitter-case-role-lambda"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}
resource "aws_iam_role_policy" "policy" {
  name   = "lambda-role-policy"
  role   = aws_iam_role.role_lambda.id
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Policy0",
            "Effect": "Allow",
            "Action": [
                "logs:DisassociateKmsKey",
                "logs:DeleteSubscriptionFilter",
                "secretsmanager:DescribeSecret",
                "logs:UntagLogGroup",
                "logs:DeleteLogGroup",
                "logs:CreateLogGroup",
                "secretsmanager:ListSecretVersionIds",
                "logs:CreateExportTask",
                "logs:PutMetricFilter",
                "secretsmanager:GetResourcePolicy",
                "logs:CreateLogStream",
                "logs:DeleteMetricFilter",
                "secretsmanager:GetSecretValue",
                "logs:TagLogGroup",
                "logs:DeleteRetentionPolicy",
                "logs:AssociateKmsKey",
                "logs:PutSubscriptionFilter",
                "logs:PutRetentionPolicy"
            ],
            "Resource": [
                "arn:aws:secretsmanager:*:${var.account_id}:secret:*",
                "arn:aws:logs:*:${var.account_id}:log-group:*"
            ]
        },
        {
            "Sid": "Policy1",
            "Effect": "Allow",
            "Action": [
                "logs:DeleteLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:${var.account_id}:log-group:*:log-stream:*"
        },
        {
            "Sid": "Policy2",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetRandomPassword",
                "logs:CreateLogDelivery",
                "logs:DeleteResourcePolicy",
                "logs:PutResourcePolicy",
                "logs:PutDestinationPolicy",
                "logs:UpdateLogDelivery",
                "logs:CancelExportTask",
                "logs:DeleteLogDelivery",
                "logs:DeleteDestination",
                "logs:PutDestination",
                "secretsmanager:ListSecrets"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api/api-gw"
}

resource "aws_lambda_function" "lambda_scan" {
  filename         = "~/twitter-case-scan.zip"
  function_name    = "twitter-case-scan"
  role             = aws_iam_role.role_lambda.arn
  handler          = "main.handler"
  source_code_hash = filebase64sha256("~/twitter-case-scan.zip")
  timeout          = 60
  runtime          = "python3.8"
}

resource "aws_lambda_function" "lambda_api" {
  filename         = "~/twitter-case-api.zip"
  function_name    = "twitter-case-api"
  role             = aws_iam_role.role_lambda.arn
  handler          = "main.handler"
  source_code_hash = filebase64sha256("~/twitter-case-api.zip")
  timeout          = 60
  runtime          = "python3.8"
}

resource "aws_api_gateway_account" "apigw" {
  cloudwatch_role_arn = aws_iam_role.apigw.arn
}

resource "aws_api_gateway_rest_api" "apigateway" {
  name = "twitter-case-api-gateway"
  endpoint_configuration {
    types = ["REGIONAL"]
    }
}


resource "aws_lambda_permission" "apigw_access_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.apigateway.execution_arn}/*/*"
}


resource "aws_api_gateway_method" "main_method" {
  rest_api_id   = aws_api_gateway_rest_api.apigateway.id
  resource_id   = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = { 
      "method.request.querystring.query" = true 
      "method.request.querystring.tag" = false
      }
}


resource "aws_api_gateway_method_response" "main_method_200" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  resource_id = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method = aws_api_gateway_method.main_method.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration" "method_integration" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  resource_id = aws_api_gateway_method.main_method.resource_id
  http_method = aws_api_gateway_method.main_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_api.invoke_arn

  depends_on = [aws_api_gateway_method.main_method]
}

resource "aws_api_gateway_integration_response" "method_integration_200" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  resource_id = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method = aws_api_gateway_method.main_method.http_method
  status_code = aws_api_gateway_method_response.main_method_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [
    aws_api_gateway_method_response.main_method_200,
    aws_api_gateway_integration.method_integration
  ]
}


resource "aws_api_gateway_method" "options_method" {
  rest_api_id   = aws_api_gateway_rest_api.apigateway.id
  resource_id   = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method   = "OPTIONS"
  authorization = "NONE"
}


resource "aws_api_gateway_method_response" "options_response" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  resource_id = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method = aws_api_gateway_method.options_method.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }

  depends_on = [aws_api_gateway_method.options_method]
}


resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  resource_id = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method = aws_api_gateway_method.options_method.http_method
  type        = "MOCK"

  request_templates = {
    "application/json" = "{ \"statusCode\": 200 }"
  }

  depends_on = [aws_api_gateway_method.options_method]
}


resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  resource_id = aws_api_gateway_rest_api.apigateway.root_resource_id
  http_method = aws_api_gateway_method.options_method.http_method
  status_code = aws_api_gateway_method_response.options_response.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [
    aws_api_gateway_method_response.options_response,
    aws_api_gateway_integration.options_integration
  ]
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.apigateway.id
  stage_name  = "api"

  depends_on = [
    aws_api_gateway_integration.method_integration,
    aws_api_gateway_integration.options_integration
  ]
}


resource "aws_db_instance" "db" {
  identifier          = "twitter-case-db"
  allocated_storage   = 20
  storage_type        = "gp2"
  engine              = "mysql"
  instance_class      = "db.t2.micro"
  name                = "twitter_case_db"
  username            = "admin"
  password            = "admin123"
  skip_final_snapshot = true
  publicly_accessible = true
}

resource "aws_secretsmanager_secret" "rds_secret" {
  name = "twitter-case-db-cred"
}

resource "aws_secretsmanager_secret_version" "rds_secret" {
  depends_on    = [aws_db_instance.db]
  secret_id     = aws_secretsmanager_secret.rds_secret.id
  secret_string = <<EOF
{
"username": "${aws_db_instance.db.username}",
"host": "${aws_db_instance.db.address}",
"password": "${aws_db_instance.db.password}",
"dbname": "${aws_db_instance.db.name}"
}  

EOF
}

resource "aws_secretsmanager_secret" "twt_secret" {
  name = "twitter-bearer-token"
}

resource "aws_secretsmanager_secret_version" "twt_secret" {
  secret_id     = aws_secretsmanager_secret.twt_secret.id
  secret_string = <<EOF
{
"token": "Bearer ${var.bearer_token}"
}
EOF
}

resource "aws_cloudwatch_event_rule" "scan_rule" {
  name                = "twitter-lambda-scan-sched"
  description         = "Scheduler for scan lambda"
  schedule_expression = "rate(12 hours)"
}
resource "aws_cloudwatch_event_target" "scan_rule" {
  rule      = aws_cloudwatch_event_rule.scan_rule.name
  target_id = "lambda"
  arn       = aws_lambda_function.lambda_scan.arn
}
resource "aws_lambda_permission" "scan_rule" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_scan.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.scan_rule.arn
}

resource "aws_cloudwatch_dashboard" "dash" {
  dashboard_name = "TwitterCaseDashboard"
  dashboard_body = <<EOF
{
"widgets": [
{
"type": "metric",
"x": 0,
"y": 0,
"width": 9,
"height": 3,
"properties": {
"metrics": [
[ "AWS/Lambda", "Errors", "FunctionName", "${aws_lambda_function.lambda_scan.function_name}", { "color": "#d62728" } ],
[ ".", "Invocations", ".", ".", { "color": "#2ca02c" } ],
[ ".", "Duration", ".", ".", { "color": "#1f77b4" } ]
],
"view": "singleValue",
"stacked": false,
"region": "${var.region}",
"title": "Lambda Scan",
"period": 3600,
"stat": "Sum"
}
},
{
"type": "metric",
"x": 9,
"y": 0,
"width": 15,
"height": 6,
"properties": {
"metrics": [
[ "AWS/RDS", "WriteThroughput", "DBInstanceIdentifier", "${aws_db_instance.db.identifier}", { "color": "#2ca02c", "yAxis": "left" } ],
[ ".", "ReadThroughput", ".", ".", { "color": "#1f77b4" } ]
],
"view": "timeSeries",
"stacked": false,
"region": "${var.region}",
"title": "RDS Read/Write",
"period": 1,
"stat": "Sum"
}
},
{
"type": "log",
"x": 0,
"y": 21,
"width": 24,
"height": 6,
"properties": {
"query": "SOURCE '/aws/lambda/${aws_lambda_function.lambda_scan.function_name}' | fields @message\n| sort @timestamp desc\n| limit 100",
"region": "${var.region}",
"stacked": false,
"view": "table",
"title": "Lambda Scan Logs"
}
},
{
"type": "metric",
"x": 0,
"y": 3,
"width": 9,
"height": 3,
"properties": {
"metrics": [
[ "AWS/Lambda", "Errors", "FunctionName", "${aws_lambda_function.lambda_api.function_name}", { "color": "#d62728" } ],
[ ".", "Invocations", ".", ".", { "color": "#2ca02c" } ],
[ ".", "Duration", ".", ".", { "color": "#1f77b4" } ]
],
"view": "singleValue",
"region": "${var.region}",
"stat": "Sum",
"period": 3600,
"title": "Lambda API"
}
},
{
"type": "log",
"x": 0,
"y": 15,
"width": 24,
"height": 6,
"properties": {
"query": "SOURCE '/aws/lambda/${aws_lambda_function.lambda_api.function_name}' | fields @message\n| sort @timestamp desc\n| limit 100",
"region": "${var.region}",
"stacked": false,
"title": "Lambda API Logs",
"view": "table"
}
},
{
"type": "log",
"x": 0,
"y": 9,
"width": 24,
"height": 6,
"properties": {
"query": "SOURCE '${aws_cloudwatch_log_group.api_gw.name}' | fields @message\n| sort @timestamp desc\n| limit 200",
"region": "${var.region}",
"stacked": false,
"title": "API Gateway Logs",
"view": "table"
}
},
{
"type": "metric",
"x": 0,
"y": 6,
"width": 24,
"height": 3,
"properties": {
"metrics": [
[ "AWS/ApiGateway", "4XXError", "ApiName", "${aws_lambda_function.lambda_api.function_name}", { "color": "#d62728" } ],
[ ".", "Count", ".", ".", { "color": "#2ca02c" } ],
[ ".", "Latency", ".", ".", { "color": "#1f77b4" } ],
[ ".", "5XXError", ".", ".", { "stat": "Average", "period": 300, "yAxis": "left" } ],
[ ".", "IntegrationLatency", ".", ".", { "stat": "Average", "period": 300, "color": "#1f77b4" } ]
],
"view": "singleValue",
"region": "${var.region}",
"title": "API Gateway Metrics",
"period": 3600,
"stat": "Sum"
}
}
]
}
EOF
}


output "RDS" {
  value = aws_db_instance.db.address
}

output "CloudWatch" {
  value = aws_cloudwatch_dashboard.dash.dashboard_name
}

output "API" {
  value = aws_api_gateway_deployment.deployment.invoke_url
}
