variable "repositories" {
  description = "A map of repository names to create"
  type        = map(string)
}

variable "image_tag_mutability" {
  description = "The tag mutability setting for the repository. Defaults to MUTABLE."
  type        = string
  default     = "MUTABLE"
}

variable "scan_on_push" {
  description = "Indicates whether images are scanned after being pushed to the repository. Defaults to false."
  type        = bool
  default     = false
}