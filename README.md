MSSQL Application Stack on Azure Function and Azure SQL
====================================================

## Requirements:

* terraform
* Azure cli "az"
* Azure tools "func"


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
```

Verify the output and when ready apply the changes: 
```
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

Return to root dir:
```cd ..```

## Test locally
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

func start
```

You may (will) need to install an ODBC driver in your dev instance to connect to DB

## publish function to Azure

```
func azure functionapp publish [sa_name]
```
