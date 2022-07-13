data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

variable "region" {
  default = "eu-west-1"
}
# variable "token"{
# }
# variable "access_key" {
# }
# variable "secret_key" {
# }

provider "aws" {
    region = var.region
#     access_key = var.access_key
#     secret_key = var.secret_key
#     token = var.token
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"


  tags = {
    Name = "HelloWorld"
  }
}
