terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

provider "snowflake" {
  role = "SYSADMIN"
}

module "databases" {
  database = var.database
  source = "../databases"
}

module "roles" {
  source = "../roles"
}

module "schemas" {
  database = var.database
  source = "../schemas"
}

module "tables" {
  database = var.database
  source = "../tables"
}

module "storage_integrations" {
  source = "../storage_integrations" 
}

module "stages" {
  database = var.database
  source = "../stages" 
}