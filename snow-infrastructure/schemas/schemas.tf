terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

variable "database" {}

resource "snowflake_schema" "schema" {
  database = "${var.database}"
  name     = "DATA"
  comment  = "streamlit schema"

  is_transient        = false
  is_managed          = false
}