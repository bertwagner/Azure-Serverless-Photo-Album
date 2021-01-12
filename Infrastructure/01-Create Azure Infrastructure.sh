#!/bin/bash

# Function app and storage account names must be unique.
resourceGroupName=serverless-photo-album-resources
storageAccountName=serverlessphotostorage
functionAppName=serverless-photo-album-app
region=eastus

printf "\nDeleting any existing resources"
# Delete everything if it exists to start fresh
{ # try
    az group delete --name $resourceGroupName --yes
} || { # catch
    printf "\nNo existing resources to delete..."
}

printf "\nCreating a resource group..."
az group create \
    --location $region \
    --name $resourceGroupName

printf "\nCreating a photo storage account..."
# We create this using the cheapest storage possible: east region, locally redundant storage
az storage account create \
    --name $storageAccountName \
    --resource-group $resourceGroupName \
    --location $region \
    --sku Standard_LRS

printf "\nUpdate storage account to allow static web hosting"
az storage blob service-properties update \
    --account-name $storageAccountName  \
    --static-website \
    --404-document 404.html \
    --index-document index.html

printf "\nCreate a container to store the blobs in"
# We make the public access level "blob" so files can be read anonymously in the browser
az storage container create \
    --name "photos" \
    --account-name $storageAccountName \
    --public-access blob \
    --resource-group $resourceGroupName

printf "\nCreating an Azure Function to retrieve photo URLs..."
az functionapp create \
    --name $functionAppName \
    --resource-group $resourceGroupName \
    --storage-account $storageAccountName \
    --consumption-plan-location $region \
    --os-type Linux \
    --functions-version 3 \
    --runtime python \
    --runtime-version 3.8 

printf "\nUpdate the function app to allow CORS origins from our storage account..."
az functionapp cors add --name $functionAppName --resource-group $resourceGroupName --allowed-origins "https://$storageAccountName.z13.web.core.windows.net"
az resource update --name web --resource-group $resourceGroupName --namespace Microsoft.Web --resource-type config --parent sites/$functionAppName --set properties.cors.supportCredentials=true

#printf "\nSetup Azure CDN to allow custom domain over HTTPS..."
#https://docs.microsoft.com/en-us/azure/storage/blobs/storage-custom-domain-name?tabs=azure-portal#map-a-custom-domain-with-https-enabled


