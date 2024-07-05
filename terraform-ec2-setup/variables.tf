# variables.tf

variable "key_name" {
  description = "Name of the SSH key pair in AWS"
  type        = string
  default     = "tcc-dev-key.pem"  # Replace with your actual key pair name
}

variable "private_key_path" {
  description = "Path to SSH private key"
  type        = string
  default     = "D:\\telco-customer-churn\\tcc-dev-key.pem" # Replace with your actual private key path
}
