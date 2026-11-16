# ------------------------------------------------------------
# Week 11 - Terraform
# Builds an Ubuntu EC2 web server with HTTP + SSH access
# ------------------------------------------------------------

# Terraform settings: which provider plugins this config needs
# and the minimum Terraform version allowed to run it
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws" # Official AWS provider from the Terraform Registry
      version = ">= 5.0"        # Updated from ~> 3.27 per instructor note
    }
  }
  required_version = ">= 0.14.9"
}

# AWS provider: uses the [default] profile in the .aws credentials
# file (Learner Lab keys) and builds everything in us-east-1
provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

# Security group (firewall) for the web server
resource "aws_security_group" "web-sg" {
  name = "web-sg"

  # Inbound HTTP (port 80) from anywhere, for web traffic
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Inbound SSH (port 22) from anywhere, so we can log in with vockey
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # All outbound traffic allowed ("-1" = all protocols)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance resource named "app_server"
resource "aws_instance" "app_server" {
  ami           = "ami-0547ecbf0e9b4aeb5" # Ubuntu Server AMI for us-east-1
  instance_type = "t2.micro"              # Small, free-tier-sized server

  # Attach the security group above to this instance
  vpc_security_group_ids = [aws_security_group.web-sg.id]

  # Use the existing Learner Lab key pair (vockey) for SSH.
  # Adding a key forces Terraform to destroy and recreate the instance.
  key_name = "vockey"

  # Name tag comes from variables.tf instead of being hard-coded
  tags = {
    Name = var.instance_name
  }
}