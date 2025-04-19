variable "aws_region" {
  default = "ap-south-1"
}

variable "ami_id" {
  type        = string
  description = "The id of the machine image (AMI) to use for the servers."
  default     = "ami-0f1dcc636b69a6438"

}

variable "ssh_public_key_dev" {
  description = "Public SSH key for Scw server"
  sensitive   = true

}