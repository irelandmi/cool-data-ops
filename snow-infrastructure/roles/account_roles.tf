terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

provider "snowflake" {
  role = "SECURITYADMIN"
}

resource "snowflake_role" "db_role" {
  name     = "STREAMLIT_ROLE"
  comment  = "terraform streamlit role"
}