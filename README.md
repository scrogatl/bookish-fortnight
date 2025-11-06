MSSQL Application Stack on Azure Function and Azure SQL
====================================================

## Create Azure Resource Group and Function App with Terraform

This terraform code borrows from the Azure Functions Quickstart examples: https://learn.microsoft.com/en-us/azure/azure-functions/functions-get-started?pivots=programming-language-python

Edit the `main.tf` file to include your IP address (range) and change the DB password:
```
locals {
  admin_password = "complex_password_here_!23" # Replace with a strong password"
}

resource "azurerm_mssql_firewall_rule" "example" {
  name             = "allow-my-ip-address"
  server_id        = azurerm_mssql_server.server.id
  start_ip_address = "104.28.241.110" # Your specific starting public IP address
  end_ip_address   = "104.28.241.150" # Your specific ending public IP address (can be the same as start for a single IP)
}
```

Get Azure credentials: 
```
export ARM_SUBSCRIPTION_ID=$(az account show --query "id" --output tsv) 
```

Use terraform to create Azure Resource Group, Function App, and Azure SQL DB:
```
cd terraform
terraform init --upgrade 
terraform plan -out main.tfplan -var="runtime_name=python" -var="runtime_version=3.12"
terraform apply main.tfplan
```

This will run for a few minutes. When finsished, you should see an output similar to this:
```
admin_password = "complex_password_here_!23 "
asp_name = "vvwzuybj"
fa_name = "vvwzuybj"
fa_url = "https://vvwzuybj.azurewebsites.net"
resource_group_name = "rg-crisp-ostrich"
sa_name = "vvwzuybj"
sql_server_name = "sql-helped-rhino"
```

Add the stored proceduures:
```
../scripts/configuresql.sh
```

## Run function

To run the function locally export the env vars:

**NOTE: the New Relic agent will not work when running locally!!**
```
cd ..
export DB_SERVER=$(terraform output  -raw sql_server_name)    
export MSSQL_SA_PASSWORD=$(terraform output  -raw admin_password)
func start
```

This project deploys a complete, observable web application and database environment into Microsoft Azure. The purpose is to create a realistic, cost-effective environment for demonstrating full-stack observability with New Relic.

The stack runs on a single Azure Virtual Machine. It consists of:

1.  **Docker Containers:**
    -   A **Python Flask application** serving the web UI and query endpoints.
    -   A **Microsoft SQL Server 2022** container that automatically restores the AdventureWorks database.
2.  **VM Services:**
    -   The **New Relic Infrastructure agent** installed as a service on the host VM, providing host and container monitoring.

The Flask application is instrumented with the New Relic APM agent, providing a complete, observable stack from the front end to the database, all running on one VM.

Architecture