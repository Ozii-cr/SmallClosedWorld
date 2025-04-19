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


################################################################################
# Security Groups
################################################################################

resource "aws_security_group" "ScwServerSG" {
  name        = "ScwerverSecurityGroup"
  description = "ScwerverSecurityGroup"
  vpc_id      = module.dev_vpc.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "allow https"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }
  ingress {
    description = "allow http"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }
  ingress {
    description = "ssh ports"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

################################################################################
# EC2
################################################################################
module "scw_server" {
  source            = "./modules/ec2-instance"
  key_name          = "ScwKey"
  ssh_public_key    = var.ssh_public_key_dev
  ami               = var.ami_id
  instance_type     = "t2.micro"
  security_group_id = aws_security_group.ScwServerSG.id
  subnet_id         = module.dev_vpc.public_subnets[0]
  instance_name     = "Scw Server"
  volume_size       = 8
  enable_eip        = false
  instance_state    = "running"
}