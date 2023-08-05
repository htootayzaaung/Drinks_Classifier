import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import time
from PIL import Image

def create_brand_folder(brand):
    brand_folder = f"Images/{brand.lower().replace(' ', '_')}_images"
    if not os.path.exists(brand_folder):
        os.makedirs(brand_folder)
    return brand_folder

def download_images_from_google(query, brand_folder, num_images=100):
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    image_urls = []
    for img in soup.find_all("img"):
        image_urls.append(img["src"])

    count = 0
    for i, img_url in enumerate(image_urls):
        try:
            img_path = os.path.join(brand_folder, f"{i}.jpg")
            urllib.request.urlretrieve(img_url, img_path)
            count += 1
            print(f"Downloaded {img_path}")

            # Open the downloaded image
            with Image.open(img_path) as img:
                # Rotate the image by 45 degrees and save it
                img_rotated_45 = img.rotate(45)
                img_rotated_45_path = os.path.join(brand_folder, f"{i}_rotated_45.jpg")
                img_rotated_45.save(img_rotated_45_path)

                # Rotate the image by 120 degrees and save it
                img_rotated_120 = img.rotate(120)
                img_rotated_120_path = os.path.join(brand_folder, f"{i}_rotated_120.jpg")
                img_rotated_120.save(img_rotated_120_path)

            if count >= num_images:
                break
            time.sleep(1)  # Add a delay between image downloads to avoid overloading the website
        except Exception as e:
            print(f"Error downloading image {i}: {e}")

if __name__ == "__main__":
    brands = ["Heineken", "Carlsberg", "Tiger"]  # Add more brands as needed

    for brand in brands:
        brand_folder = create_brand_folder(brand)
        query = f"{brand} can"  # You can modify the query as per your requirement
        download_images_from_google(query, brand_folder, num_images=100)
