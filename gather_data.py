import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import time
from PIL import Image
import flickrapi
from pexels_api import API

def create_brand_folder(brand):
    brand_folder = f"Images/{brand.lower().replace(' ', '_')}_images"
    if not os.path.exists(brand_folder):
        os.makedirs(brand_folder)
    return brand_folder

#############################################       UNSPLASH       #############################################

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
                else:
                    print(f"Error downloading image {i}: HTTP {img_response.status_code}")
            except Exception as e:
                print(f"Error downloading image {i}: {e}")
            time.sleep(1)  # Add a delay between image downloads to avoid overloading the API

#############################################       END OF UNSPLASH       #############################################


#############################################        FLICKR       #############################################

def download_images_from_flickr(query, brand_folder, num_images=100, api_key=None, api_secret=None):
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    photos = flickr.photos.search(text=query, per_page=num_images, sort='relevance')

    for i, photo in enumerate(photos['photos']['photo']):
        photo_url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
        try:
            img_path = os.path.join(brand_folder, f"flickr_{i}.jpg")
            img_response = requests.get(photo_url)
            if img_response.status_code == 200:
                with open(img_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Downloaded {img_path}")
            else:
                print(f"Error downloading image {i}: HTTP {img_response.status_code}")
        except Exception as e:
            print(f"Error downloading image {i}: {e}")
        time.sleep(1)  # Add a delay between image downloads to avoid overloading the API


#############################################       END OF FLICKR       #############################################

#############################################       MAIN FUNCTION       #############################################

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
    api_key = "7dffe0a73bba4d9e5671fb934e2a6d62"  # Replace with your actual Flickr API key
    api_secret = "b1e876ee5fb6acbd"  # Replace with your actual Flickr API secret

    for brand in brands:
        brand_folder = create_brand_folder(brand)
        query = brand  # Use the brand name itself for Red Bull, Coca Cola, and Pepsi
        download_images_from_unsplash(query, brand_folder, num_images=100, access_key=access_key)
        download_images_from_flickr(query, brand_folder, num_images=100, api_key=api_key, api_secret=api_secret)

#############################################       END OF MAIN FUNCTION       #############################################
