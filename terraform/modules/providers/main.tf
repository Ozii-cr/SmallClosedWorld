provider "aws" {
  region = var.aws_provider_region

  default_tags {
    tags = {
      Terraform   = "true"
      Environment = var.provider_environment
    }
  }
}


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50.0"
    }
  }
}