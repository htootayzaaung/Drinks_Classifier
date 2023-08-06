import os
from PIL import Image

def rotate_images_in_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(folder, filename)
            with Image.open(image_path) as img:
                # Convert the image to RGB mode (removing the palette)
                img_rgb = img.convert("RGB")

                # Rotate the image by 45 degrees and save it
                img_rotated_45 = img_rgb.rotate(45)
                img_rotated_45_path = os.path.join(folder, f"{filename}_rotated_45.jpg")
                img_rotated_45.save(img_rotated_45_path)
                print(f"Saved {img_rotated_45_path}")

                # Rotate the image by 120 degrees and save it
                img_rotated_120 = img_rgb.rotate(120)
                img_rotated_120_path = os.path.join(folder, f"{filename}_rotated_120.jpg")
                img_rotated_120.save(img_rotated_120_path)
                print(f"Saved {img_rotated_120_path}")

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
        rotate_images_in_folder(brand_folder)
