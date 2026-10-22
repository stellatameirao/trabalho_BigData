terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aiven = {
      source  = "aiven/aiven"
      version = "~> 4.62.0"
    }
  }
}

provider "aiven" {}

resource "aiven_pg" "eleicoes" {
  project      = var.project_name
  service_name = var.service_name
  cloud_name   = var.cloud_name
  plan         = var.service_plan

  lifecycle {
    prevent_destroy = true
  }
}