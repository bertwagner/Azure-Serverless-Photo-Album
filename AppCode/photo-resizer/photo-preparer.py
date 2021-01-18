import argparse
import os
import pathlib
import cv2

def create_thumbs_folder(folder_path):
    thumbs_path = pathlib.Path(os.path.join(folder_path,"thumbs"))
    
    # Create the thumbs folder if doesn't already exist
    thumbs_path.mkdir(exist_ok=True)

    return thumbs_path

def rename_filename_with_dimensions(folder,file_root,file_extension):
    filename = os.path.join(folder,file_root+file_extension)

    # Get photo dimensions
    photo = cv2.imread(filename)
    width = photo.shape[1]
    height = photo.shape[0]
    dimensions = f"{width}x{height}"

    # Append photo dimensions if they don't exist 
    file_root_with_dimensions = f"{file_root}"
    filename_with_dimensions = file_root+file_extension
    if not file_root.endswith(dimensions):
        file_root_with_dimensions = f"{file_root} {dimensions}"
        filename_with_dimensions = f"{file_root_with_dimensions}{file_extension}"
        
        # Rename file
        os.rename(filename,os.path.join(folder,filename_with_dimensions))
    

    return filename_with_dimensions,file_root_with_dimensions

def calculate_thumnail_dimensions(width,height,final_max_dimension):
    if width > height:
        new_width = final_max_dimension
        new_height = int((final_max_dimension * height) / width)
    else:
        new_width = int((final_max_dimension * width) / height)
        new_height = final_max_dimension
    
    return (new_width,new_height)

def create_thumbnail(folder, thumbs_folder, file_root, file_root_with_dimensions, file_extension):

    filename = os.path.join(folder,file_root+file_extension)

    # Get photo dimensions
    photo = cv2.imread(os.path.join(folder,file_root_with_dimensions+file_extension))
    width = photo.shape[1]
    height = photo.shape[0]

    thumb_dimensions = calculate_thumnail_dimensions(width,height,200)
 
    # Resize image
    resized_image = cv2.resize(photo,thumb_dimensions,interpolation=cv2.INTER_CUBIC)

    # file_root may already have dimensions appended if previously processed - strip the dimensions
    file_parts = file_root.split()
    file_root = " ".join(file_parts[:-1]) if len(file_parts) > 1 else file_parts[0]

    # Name the file
    dimensions = f"{thumb_dimensions[0]}x{thumb_dimensions[1]}"
    thumbnail_file = f"{file_root} {dimensions}{file_extension}"
    thumbnail_filename = os.path.join(thumbs_folder,thumbnail_file)

    # Save thumbnail
    cv2.imwrite(thumbnail_filename,resized_image)


if __name__ == "__main__":
    # Parse the folder path from command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()
    folder = args.folder

    # Create a thumbs folder if it doesn't exist
    thumbs_folder = create_thumbs_folder(folder)

    # Iterate over each file
    photo_extensions = [".gif",".png",".tif",".jpg",".jpeg"]
    for file in os.listdir(folder):
        filename = os.fsdecode(file)

        if any(extension in filename for extension in photo_extensions):
        
            file_root, file_extension = os.path.splitext(filename)

            filename_with_dimensions, file_root_with_dimensions = rename_filename_with_dimensions(folder,file_root,file_extension)

            create_thumbnail(folder, thumbs_folder, file_root, file_root_with_dimensions, file_extension)

            # Upload all files to Azure