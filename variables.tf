variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "aws-sample"
}

variable "key_pair_name" {
  description = "Name of existing AWS key pair for EC2 access"
  type        = string
  default     = "my-key-pair"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "allowed_cidr" {
  description = "CIDR block allowed to access EC2 instance"
  type        = string
  default     = "0.0.0.0/0"
}