# Week 12 - Terraform + Lambda
# Deploys Lambda functions that stop / start EC2 instances
# State is stored in Terraform Cloud

# Terraform settings: required provider, minimum CLI version,
# and Terraform Cloud as the place where state is stored
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws" # Official AWS provider
      version = ">= 5.0"        # Updated from ~> 3.27 per instructor note
    }
  }
  required_version = ">= 0.14.9"

  # Store state in Terraform Cloud instead of a local terraform.tfstate file
  cloud {
    organization = "mustaf-adv-scripting-cloud" # Must match your org name exactly

    workspaces {
      name = "mustaf-week12" # Workspace gets created automatically on init
    }
  }
}

# AWS provider: region only. profile was removed because runs now happen
# in Terraform Cloud, which gets AWS keys from workspace environment variables.
provider "aws" {
  region = "us-east-1"
}

# Data source: look up the existing LabRole. We can't create IAM roles
# in the Learner Lab, so Lambda reuses this one for its permissions.
data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

# Lambda function that stops every running EC2 instance
resource "aws_lambda_function" "stop_ec2" {
  filename         = "stopEC2.zip"                   # Zipped Python code
  source_code_hash = filebase64sha256("stopEC2.zip") # Redeploys when the zip changes
  function_name    = "mustaf-stop-ec2"               # Includes my first name
  role             = data.aws_iam_role.lab_role.arn  # Permissions come from LabRole
  runtime          = "python3.12"                    # python3.9 is retired on Lambda
  handler          = "stopEC2.lambda_handler"        # <file name>.<function name>
  timeout          = 30                              # Default 3 seconds can be too short
}

# Step 4: Lambda function that starts every stopped EC2 instance
resource "aws_lambda_function" "start_ec2" {
  filename         = "startEC2/startEC2.zip"                   # Zipped Python code in the startEC2 folder
  source_code_hash = filebase64sha256("startEC2/startEC2.zip") # Redeploys when the zip changes
  function_name    = "mustaf-start-ec2"                        # Includes my first name
  role             = data.aws_iam_role.lab_role.arn            # Same LabRole permissions
  runtime          = "python3.12"                              # Current Python runtime
  handler          = "startEC2.lambda_handler"                 # <file name>.<function name>
  timeout          = 30                                        # Default 3 seconds can be too short
}