terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

variable "database" {}

resource "snowflake_database" "db" {
  name = "${var.database}"
}

output "database" {
	value = "${var.database}"
}