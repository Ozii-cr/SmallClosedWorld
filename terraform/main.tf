module "required_providers" {
  source               = "./modules/providers"
  aws_provider_region  = var.aws_region
  provider_environment = "dev"
}

################################################################################
# Ecr repositories
################################################################################
module "ecr_repositories" {
  source = "./modules/ecr-repository"

  repositories = {
    scw-app = "scw-app"
  }

  image_tag_mutability = "MUTABLE"
  scan_on_push         = false
}


################################################################################
# Vpc with public subnets
################################################################################
module "dev_vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.10.0"

  name = "scw-dev-vpc"
  cidr = "10.1.0.0/16"

  azs = [
    "${var.aws_region}a",
    "${var.aws_region}b"
  ]

  public_subnets = ["10.1.101.0/24", "10.1.102.0/24"]

  enable_nat_gateway = false
  single_nat_gateway = false
  enable_vpn_gateway = false
}
