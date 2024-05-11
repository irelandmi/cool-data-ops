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

data "local_file" "config" {
  filename = "${path.module}/../../secrets/config.yml"
}

# Decode the YAML content to a map
locals {
  config_data = yamldecode(data.local_file.config.content)
  integration_config = local.config_data["config"]["integration"]
}

resource "snowflake_stage" "example_stage" {
  name        = "KRAKEN_BATCHES_STAGE"
  url         = local.integration_config["datalake"]["storage_allowed_locations"]
  database    = "${var.database}"
  schema      = "DATA"
  storage_integration = "DATALAKE"
}