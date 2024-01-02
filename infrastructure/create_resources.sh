# Variables, you can change these if you want
resourceGroupName="trading-bot-rg"
functionAppName="trading-bot-function-app"
storageAccountName="tradingbotstorageaccount"
location="westeurope"

# Create a resource group
az group create --name $resourceGroupName --location $location

# Create a storage account
az storage account create --name $storageAccountName --location $location --resource-group $resourceGroupName --sku Standard_LRS

# Retrieve the storage account connection string
storageConnectionString=$(az storage account show-connection-string --name $storageAccountName --resource-group $resourceGroupName --query connectionString --output tsv)

# Create a consumption plan function app with Python 3.8
az functionapp create \
  --name $functionAppName \
  --resource-group $resourceGroupName \
  --storage-account $storageAccountName \
  --consumption-plan-location $location \
  --runtime python \
  --runtime-version 3.8 \
  --functions-version 4 \
  --os-type Linux \
  --disable-app-insights true

# Configure the storage connection string in the function app
az functionapp config appsettings set \
  --name $functionAppName \
  --resource-group $resourceGroupName \
  --settings AzureWebJobsStorage=$storageConnectionString