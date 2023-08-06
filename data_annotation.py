import os
import subprocess

def annotate_with_labelimg(folder):
    print(f"Annotating images in {folder} with LabelImg")
    labelimg_command = f"labelImg {folder}"
    subprocess.call(labelimg_command, shell=True)

def annotate_with_via(folder):
    print(f"Annotating images in {folder} with VIA")
    via_command = f"via {folder}"
    subprocess.call(via_command, shell=True)

if __name__ == "__main__":
    brands = [
        "Heineken beer",
        "Carlsberg beer",
        "Tiger beer",
        "Red Bull energy drink",
        "Coca Cola",
        "Pepsi"
    ]  # Add more brands as needed

    for brand in brands:
        brand_folder = f"Images/{brand.lower().replace(' ', '_')}_images"
        # Annotate the original downloaded images
        annotate_with_labelimg(brand_folder)

        # Annotate the data-augmented images
        augmented_folder = f"{brand_folder}_augmented"
        if os.path.exists(augmented_folder):
            annotate_with_labelimg(augmented_folder)

        print(f"Annotation for {brand} completed.")
