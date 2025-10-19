variable "deploy_user" {
  type        = string
  description = "SSH user on the remote server"
}

variable "deploy_host" {
  type        = string
  description = "IP or hostname of the remote server"
}

variable "ssh_private_key" {
  type        = string
  description = "Private SSH key used for authentication"
  sensitive   = true
}

variable "env_vars" {
  type        = string
  description = "Environment variables to create the .env file"
  sensitive   = true
}
