terraform {
  backend "s3" {
    bucket  = "bucket"
    region  = "eu-west-1"
    profile = "default"
    key     = "infra/terraform.tfstate"
  }

}
provider "aws" {
  region = "eu-west-1"
}

provider "aws" {
  alias = "frankfurt"
  region  = "eu-central-1"
}
