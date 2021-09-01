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

variable "datadog_role" {
  type    = string
  default = "DatadogAWSIntegrationRole"
}

variable "datadog_app_key" {
  type = string
}

provider "aws" {
  region = "us-east-1"
}

provider "datadog" {}
