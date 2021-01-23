# Azure-Serverless-Photo-Album

A serverless photo album running on Azure.

## Build Instructions

1. [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) (I'm using WSL, so remaining documentation will be Linux based).
2. Login with `az login`.
3. Create your resource group and other infrastructure by running `bash Infrastructure/01-Create Azure Infrastructure.sh`.
4. Fix any errors you receive from the above step (likely names of some resources need to be unique across azure and already exist)
5. Install [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools) to assist with authoring and deploying function code.
6. Create a new function with func init.
7. If you need to create additional functions or debug the existing one, follow these [instructions on activating the virtual environment and debugging](https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash%2Cbrowser).
8. Installing [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/) makes viewing data easier.
9. Install `pip install azure-store-blob`, the SDK allowing python to read files from Blob storage.  Documentatino here: https://docs.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python
10. Add the storage access key to the `AzureWebJobsStorage` value in local.settings.json. 
