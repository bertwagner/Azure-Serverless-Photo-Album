import argparse
import os
import pathlib
import cv2

def create_thumbs_folder(folder_path):
    thumbs_path = pathlib.Path(os.path.join(folder_path,"thumbs"))
    
    # Create the thumbs folder if doesn't already exist
    thumbs_path.mkdir(exist_ok=True)

if __name__ == "__main__":
    # Parse the folder path from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()

    # Create a thumbs folder if it doesn't exist
    create_thumbs_folder(args.folder)

    # Iterate over each file
    for file in os.listdir(args.folder):
        filename = os.fsdecode(file)

    # Loop over all files

    # Check if file has dimensions in name
    # if not, rename to include dimensions

    # check if thumbs folder exists, create it if it doesn't

    # check if this same file exists in the thumb folder
    # if not, resize the image and put it in the thumbs folder with dimensions in name

    # Upload all files to Azure