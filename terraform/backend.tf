terraform {

  backend "s3" {
    bucket       = ""
    key          = "dev/terraform.tfstate"
    encrypt      = true
    region       = "ap-south-1"
    use_lockfile = true
  }
}