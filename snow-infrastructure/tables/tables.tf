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

resource "snowflake_table" "table" {
  database = "${var.database}"
  schema = "DATA"
  name = "DOCUMENTS"

  column {
    name = "ID"
    type = "NUMBER(38,0)"
    nullable = false

    identity {
      start_num = 1
      step_num = 1
    }
  }

  column {
    name = "DOCUMENT_STRING"
    type = "VARCHAR(16777216)"
    nullable = false
  }

  column {
    name = "DOCUMENT_VECTOR"
    type = "VARIANT"
    nullable = false
  }
}