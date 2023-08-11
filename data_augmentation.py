import os
from PIL import Image

def rotate_mirror_and_save(img_rgb, angle, filename, folder):
    base_name, ext = os.path.splitext(filename)  # Split the filename and its extension
    img_rotated = img_rgb.rotate(angle)
    img_rotated_path = os.path.join(folder, f"{base_name}_rotated_{angle}{ext}")
    img_rotated.save(img_rotated_path)
    print(f"Saved {img_rotated_path}")

def augment_images_in_folder(folder):
    # Allowed extensions tuple
    allowed_extensions = ('.webp', '.jpg', '.png')
    
    for filename in os.listdir(folder):
        if filename.endswith(allowed_extensions):  # Check if the file has an allowed extension
            image_path = os.path.join(folder, filename)
            
            with Image.open(image_path) as img:
                # Convert the image to RGB mode (removing the palette)
                img_rgb = img.convert("RGB")
                base_name, ext = os.path.splitext(filename)  # Split the filename and its extension

                # Mirror the image (horizontal flip) and save it
                img_mirrored = img_rgb.transpose(Image.FLIP_LEFT_RIGHT)
                img_mirrored_path = os.path.join(folder, f"{base_name}_mirrored{ext}")
                img_mirrored.save(img_mirrored_path)
                print(f"Saved {img_mirrored_path}")

                # Rotate the image by 5 degrees (counter-clockwise) and save it
                rotate_mirror_and_save(img_rgb, -5, filename, folder)

                # Rotate the image by 5 degrees (clockwise) and save it
                rotate_mirror_and_save(img_rgb, 5, filename, folder)

if __name__ == "__main__":
    brands = [
        "Heineken beer",
        "Coca Cola",
        "Pepsi"
    ]

    for brand in brands:
        brand_folder = f"Images/{brand.lower().replace(' ', '_')}_images"
        augment_images_in_folder(brand_folder)
