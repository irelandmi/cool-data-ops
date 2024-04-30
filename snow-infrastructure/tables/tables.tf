terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

variable "database" {
  
}

resource "snowflake_schema" "schema" {
  database = "${var.database}"
  name                = "schema"
  data_retention_days = 1
}