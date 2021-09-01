terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.56.0"
    }

    datadog = {
      source  = "DataDog/datadog"
      version = "3.3.0"
    }
  }
}

// Providers
provider "aws" {
  region = "us-east-1"
}

provider "datadog" {}

// Variables
variable "aws_account_id" {
  type = string
}

variable "datadog_aws_integration_external_id" {
  type = string
}

variable "datadog_aws_integration_policy" {
  type    = string
  default = "DatadogAWSIntegrationPolicy"
}

variable "datadog_aws_integration_role" {
  type    = string
  default = "DatadogAWSIntegrationRole"
}

variable "lambda_dir" {
  type    = string
  default = "lambda"
}

variable "lambda_python_runtime" {
  type    = string
  default = "python3.9"
}

variable "lambda_python_handler" {
  type    = string
  default = "lambda_function.lambda_handler"
}

variable "zip_file" {
  type    = string
  default = "leaky-cache.zip"
}

// Data
data "archive_file" "memory_leak" {
  type        = "zip"
  source_dir  = "${path.module}/${var.lambda_dir}"
  output_path = "${path.module}/${var.zip_file}"
}

// AWS resources
resource "aws_s3_bucket" "lambda_archives" {}

resource "aws_iam_role" "lambda_exec" {
  name = "serverless_lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_s3_bucket_object" "memory_leak_lambda" {
  bucket = aws_s3_bucket.lambda_archives.id
  key    = var.zip_file
  source = data.archive_file.memory_leak.output_path
  etag   = filemd5(data.archive_file.memory_leak.output_path)
}

resource "aws_lambda_function" "memory_leak" {
  function_name    = "PythonMemoryLeak"
  s3_bucket        = aws_s3_bucket.lambda_archives.id
  s3_key           = aws_s3_bucket_object.memory_leak_lambda.key
  runtime          = var.lambda_python_runtime
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.memory_leak.output_base64sha256
  role             = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      DEFAULT_NAME = "world"
    }
  }
}

// AWS + Datadog data + resources
data "aws_iam_policy_document" "datadog_aws_integration_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::464622532012:root"]
    }

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values = [
        var.datadog_aws_integration_external_id
      ]
    }
  }
}

data "aws_iam_policy_document" "datadog_aws_integration" {
  statement {
    actions = [
      "apigateway:GET",
      "autoscaling:Describe*",
      "budgets:ViewBudget",
      "cloudfront:GetDistributionConfig",
      "cloudfront:ListDistributions",
      "cloudtrail:DescribeTrails",
      "cloudtrail:GetTrailStatus",
      "cloudtrail:LookupEvents",
      "cloudwatch:Describe*",
      "cloudwatch:Get*",
      "cloudwatch:List*",
      "codedeploy:List*",
      "codedeploy:BatchGet*",
      "directconnect:Describe*",
      "dynamodb:List*",
      "dynamodb:Describe*",
      "ec2:Describe*",
      "ecs:Describe*",
      "ecs:List*",
      "elasticache:Describe*",
      "elasticache:List*",
      "elasticfilesystem:DescribeFileSystems",
      "elasticfilesystem:DescribeTags",
      "elasticfilesystem:DescribeAccessPoints",
      "elasticloadbalancing:Describe*",
      "elasticmapreduce:List*",
      "elasticmapreduce:Describe*",
      "es:ListTags",
      "es:ListDomainNames",
      "es:DescribeElasticsearchDomains",
      "fsx:DescribeFileSystems",
      "fsx:ListTagsForResource",
      "health:DescribeEvents",
      "health:DescribeEventDetails",
      "health:DescribeAffectedEntities",
      "kinesis:List*",
      "kinesis:Describe*",
      "lambda:GetPolicy",
      "lambda:List*",
      "logs:DeleteSubscriptionFilter",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:DescribeSubscriptionFilters",
      "logs:FilterLogEvents",
      "logs:PutSubscriptionFilter",
      "logs:TestMetricFilter",
      "organizations:DescribeOrganization",
      "rds:Describe*",
      "rds:List*",
      "redshift:DescribeClusters",
      "redshift:DescribeLoggingStatus",
      "route53:List*",
      "s3:GetBucketLogging",
      "s3:GetBucketLocation",
      "s3:GetBucketNotification",
      "s3:GetBucketTagging",
      "s3:ListAllMyBuckets",
      "s3:PutBucketNotification",
      "ses:Get*",
      "sns:List*",
      "sns:Publish",
      "sqs:ListQueues",
      "states:ListStateMachines",
      "states:DescribeStateMachine",
      "support:*",
      "tag:GetResources",
      "tag:GetTagKeys",
      "tag:GetTagValues",
      "xray:BatchGetTraces",
      "xray:GetTraceSummaries"
    ]

    resources = ["*"]
  }
}

resource "aws_iam_policy" "datadog_aws_integration" {
  name   = var.datadog_aws_integration_policy
  policy = data.aws_iam_policy_document.datadog_aws_integration.json
}

resource "aws_iam_role" "datadog_aws_integration" {
  name               = var.datadog_aws_integration_role
  assume_role_policy = data.aws_iam_policy_document.datadog_aws_integration_assume_role.json
}

resource "aws_iam_role_policy_attachment" "datadog_aws_integration" {
  role       = aws_iam_role.datadog_aws_integration.name
  policy_arn = aws_iam_policy.datadog_aws_integration.arn
}

// Datadog resources
/*
resource "datadog_integration_aws" "python_memory_leak" {
  account_id = var.aws_account_id
  role_name  = var.datadog_aws_integration_role
}

resource "datadog_integration_aws_lambda_arn" "python_memory_leak_lambda" {
  account_id = var.aws_account_id
  lambda_arn = aws_lambda_function.memory_leak.arn
}
*/
