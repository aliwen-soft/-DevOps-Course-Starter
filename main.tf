terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.92"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "Softwire21_AliceWenban_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmos-db-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level = "BoundedStaleness"
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  lifecycle { prevent_destroy = true }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-cosmos-mongo-db"
  resource_group_name = azurerm_cosmosdb_account.main.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
}


resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-todo-app"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_app_service_plan.main.id

  site_config {
    linux_fx_version = "DOCKER|aliwen/todo_app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "GH_CLIENT_ID"               = "${var.github_id}"
    "GH_CLIENT_SECRET"           = "${var.github_secret}"
    "SECRET_TODO"                = "${var.todo_secret}"
    "TODO_CONNECTION_STRING"     = azurerm_cosmosdb_account.main.connection_strings[0]
    "TODO_DB_NAME"               = azurerm_cosmosdb_mongo_database.main.name
  }
}

