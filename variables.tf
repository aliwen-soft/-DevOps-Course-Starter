variable "prefix" {
    default = "aliwen"
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "ukwest"
}

variable "GITHUB_ID" {
  default   = "84146538b09bfb3175d6"
  sensitive = true
}

variable "GITHUB_SECRET" {
  sensitive = true
}

variable "TODO_SECRET" {
  sensitive = true
}

