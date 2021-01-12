import os
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Get HTTP parameters from URL, setting defaults if empty
    folder = req.params.get('folder')

    # Lookup the folder and return a list of blobs
    container = ContainerClient.from_connection_string(conn_str=os.environ["AzureWebJobsStorage"], container_name="photos")
    blob_list = container.list_blobs(name_starts_with=folder)

    # Create our response obejct
    photo_response = {
        "files": []
    }

    # Iterate the list to populate it
    for blob in blob_list:
        photo_response["files"].append(blob.name)
        
    
    return func.HttpResponse(
        json.dumps(photo_response),
        status_code=200,
        mimetype="application/json"
    )
