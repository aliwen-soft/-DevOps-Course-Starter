variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "ukwest"
}

variable "github_id" {
  default   = "84146538b09bfb3175d6"
  sensitive = true
}

variable "github_secret" {
  sensitive = true
}

variable "todo_secret" {
  sensitive = true
}

