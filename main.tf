terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.56.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_role"
  path               = "/"
  assume_role_policy = file("${path.module}/deploy/lambda-role-policy.json")
}
