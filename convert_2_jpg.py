import os
from PIL import Image

def convert_image_to_jpg(image_path, output_path):
    with Image.open(image_path) as img:
        if img.mode == 'P':  # Palette mode
            img_rgba = img.convert('RGBA')  # Convert palette image to RGBA
            img_rgb = Image.new("RGB", img_rgba.size, (255, 255, 255))  # Create an RGB image with a white background
            img_rgb.paste(img_rgba, mask=img_rgba.split()[3])  # Paste the RGBA image onto the RGB image using alpha channel as mask
        else:
            img_rgb = img.convert('RGB')
        img_rgb.save(output_path, 'JPEG')

def process_images_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        
        # Check if it's a supported format
        if filename.endswith(('.webp', '.png', '.jpeg', '.jpg')):
            # Create new filename with .jpg extension
            new_filename = os.path.splitext(filename)[0] + '.jpg'
            new_file_path = os.path.join(folder, new_filename)

            # If the image is already a .jpg and the filename isn't the same (due to possible name clashes)
            # skip the conversion to avoid unnecessary work
            if file_path != new_file_path or filename.endswith(('.webp', '.png', '.jpeg')):
                convert_image_to_jpg(file_path, new_file_path)

            # If the current image isn't a .jpg, remove the original after conversion
            if not filename.endswith('.jpg'):
                os.remove(file_path)

if __name__ == "__main__":
    base_dir = os.path.join(os.path.expanduser("~"), "Desktop", "Drinks_Classifier", "Images")
    
    brands = ["coca_cola_images", "heineken_beer_images", "pepsi_images"]

    for brand in brands:
        brand_folder = os.path.join(base_dir, brand)
        process_images_in_folder(brand_folder)
