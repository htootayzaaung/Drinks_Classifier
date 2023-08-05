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
        if img.get("src"):
            image_urls.append(img["src"])

    num_attempts = num_images // len(image_urls) + 1
    for _ in range(num_attempts):
        response = requests.get(search_url + f"&start={len(image_urls)}", headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        for img in soup.find_all("img"):
            if img.get("src"):
                image_urls.append(img["src"])

        time.sleep(1)  # Add a delay between requests to avoid overloading the website

    count = 0
    for i, img_url in enumerate(image_urls):
        try:
            if img_url.startswith("http"):
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

def download_images_from_unsplash(query, brand_folder, num_images=100, access_key=None):
    api_url = f"https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {access_key}",
    }

    params = {
        "query": query,
        "per_page": num_images,
    }

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        for i, image_data in enumerate(data["results"]):
            img_url = image_data["urls"]["full"]
            try:
                img_path = os.path.join(brand_folder, f"unsplash_{i}.jpg")
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(img_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"Downloaded {img_path}")

                    # Open the downloaded image
                    with Image.open(img_path) as img:
                        # Rotate the image by 45 degrees and save it
                        img_rotated_45 = img.rotate(45)
                        img_rotated_45_path = os.path.join(brand_folder, f"unsplash_{i}_rotated_45.jpg")
                        img_rotated_45.save(img_rotated_45_path)

                        # Rotate the image by 120 degrees and save it
                        img_rotated_120 = img.rotate(120)
                        img_rotated_120_path = os.path.join(brand_folder, f"unsplash_{i}_rotated_120.jpg")
                        img_rotated_120.save(img_rotated_120_path)
                else:
                    print(f"Error downloading image {i}: HTTP {img_response.status_code}")
            except Exception as e:
                print(f"Error downloading image {i}: {e}")
            time.sleep(1)  # Add a delay between image downloads to avoid overloading the API

    else:
        print(f"Failed to fetch images. HTTP {response.status_code}")

if __name__ == "__main__":
    brands = [
        "Heineken beer",
        "Carlsberg beer",
        "Tiger beer",
        "Red Bull energy drink",
        "Coca Cola",
        "Pepsi"
    ]  # Add more brands as needed

    access_key = "M9JmKwZ5nDm20hVbXpbJH8ju1bMSLtmsp7CovYk6UBo"  # Replace with your actual Unsplash access key

    for brand in brands:
        brand_folder = create_brand_folder(brand)
        query = brand  # Use the brand name itself for Red Bull, Coca Cola, and Pepsi
        download_images_from_unsplash(query, brand_folder, num_images=100, access_key=access_key)
        download_images_from_google(query, brand_folder, num_images=100)
