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
