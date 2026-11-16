# Input variable for the EC2 Name tag.
# Keeps the server name out of main.tf so it can be changed in one place.
variable "instance_name" {
  description = "Value of the Name tag for the EC2 instance"
  type        = string
  default     = "Mustaf-Server"
}