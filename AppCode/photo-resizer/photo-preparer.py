import argparse
import os
import pathlib
import cv2
from dotenv import load_dotenv, find_dotenv
from azure.storage.blob import BlobClient
import json

def create_thumbs_folder(folder_path):
    thumbs_path = pathlib.Path(os.path.join(folder_path,"thumbs"))
    
    # Create the thumbs folder if doesn't already exist
    thumbs_path.mkdir(exist_ok=True)

    return thumbs_path

def get_image_dimensions(folder,filename):
    filename = os.path.join(folder,filename)

    # Get photo dimensions
    photo = cv2.imread(filename)
    width = photo.shape[1]
    height = photo.shape[0]
    
    return width, height

def calculate_thumnail_dimensions(width,height,final_max_dimension):
    if width > height:
        new_width = final_max_dimension
        new_height = int((final_max_dimension * height) / width)
    else:
        new_width = int((final_max_dimension * width) / height)
        new_height = final_max_dimension
    
    return (new_width,new_height)

def create_thumbnail(folder, thumbs_folder, filename):

    # Get photo dimensions
    photo = cv2.imread(os.path.join(folder,filename))
    width = photo.shape[1]
    height = photo.shape[0]

    thumb_dimensions = calculate_thumnail_dimensions(width,height,200)
 
    # Resize image
    resized_image = cv2.resize(photo,thumb_dimensions,interpolation=cv2.INTER_CUBIC)

    # Save thumbnail
    cv2.imwrite(os.path.join(thumbs_folder,filename),resized_image)
    
    return resized_image, thumb_dimensions[0], thumb_dimensions[1]

def upload_to_blob_storage(local_folder, filename, blob_folder_name):
   
    blob = BlobClient.from_connection_string(conn_str=os.environ["AzureWebJobsStorage"], container_name="photos", blob_name=os.path.join(blob_folder_name,filename))

    with open(os.path.join(local_folder,filename), "rb") as data:
        blob.upload_blob(data)


if __name__ == "__main__":
    # Parse the folder path from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("name")
    args = parser.parse_args()
    folder = args.folder
    name = args.name
    
    # Load entries from .env for Azure blob storage credentials
    # The .env file should contain a value like:
    # AzureWebJobsStorage="DefaultEndpointsProtocol=https;AccountName=...<rest of connection string>..."
    dotenv_path = find_dotenv() 
    load_dotenv(dotenv_path)

    # Create a thumbs folder if it doesn't exist
    thumbs_folder = create_thumbs_folder(folder)

    # Declare an object for storing all of our photo meta data
    file_paths = []

    # Iterate over each file
    photo_extensions = [".gif",".png",".tif",".jpg",".jpeg"]
    for file in os.listdir(folder):
        filename = os.fsdecode(file)

        if any(extension in filename for extension in photo_extensions):
            file_info = {}
            file_info["name"] = filename

            width, height = get_image_dimensions(folder,filename)
            file_info["width"] = width
            file_info["height"] = height

            # Create a thumbnail, returning the thumbnail and dimensions
            thumbnail_filename, thumbnail_width, thumbnail_height = create_thumbnail(folder, thumbs_folder, filename)
            file_info["thumbnail_width"] = thumbnail_width
            file_info["thumbnail_height"] = thumbnail_height

            #upload_to_blob_storage(folder, filename, name)
            #upload_to_blob_storage(folder+"/thumbs", filename, name+"/thumbs")

            file_paths.append(file_info)

    # Save the image meta data to a json file and upload to blob storage
    json_filename = os.path.join(folder,"photos.json")
    with open(json_filename,"w") as f:
        json.dump(file_paths,f)
    upload_to_blob_storage(folder, "photos.json", name)