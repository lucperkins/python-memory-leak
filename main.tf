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

variable "aws_account_id" {
  type = string
}

variable "datadog_aws_integration_external_id" {
  type = string
}

variable "datadog_role" {
  type    = string
  default = "DatadogAWSIntegrationRole"
}

provider "aws" {
  region = "us-east-1"
}

provider "datadog" {}
