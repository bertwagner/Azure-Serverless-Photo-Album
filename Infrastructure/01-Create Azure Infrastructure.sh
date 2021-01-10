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

printf "\nDeploying the function app code..."
# cd AppCode/FunctionAlbumPhotos/AlbumPhotos
# func azure functionapp publish album-photos