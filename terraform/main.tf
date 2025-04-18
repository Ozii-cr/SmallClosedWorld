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
