terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.87"
    }
  }
}

data "local_file" "config" {
  filename = "${path.module}/../../secrets/config.yml"
}

# Decode the YAML content to a map
locals {
  config_data = yamldecode(data.local_file.config.content)
  integration_config = local.config_data["config"]["integration"]
}

resource "snowflake_storage_integration" "integration" {
  name    = "DATALAKE"
  comment = "AWS S3 Storage Integration for DataLake"
  type    = "EXTERNAL_STAGE"

  enabled = true

  storage_allowed_locations = [local.integration_config["datalake"]["storage_allowed_locations"]]
  #   storage_blocked_locations = [""]
  #   storage_aws_object_acl    = "bucket-owner-full-control"

  storage_provider         = "S3"
  # storage_aws_external_id  = "..."
#   storage_aws_iam_user_arn = "..."
  storage_aws_role_arn = local.integration_config["datalake"]["aws_role"]

}