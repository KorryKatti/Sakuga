import requests
import os
# dotenv support
from dotenv import load_dotenv

# Set up your API key
API_KEY = os.getenv("pix_api_key")  
BASE_URL = 'https://pixabay.com/api/'

# Expanded list of queries (categories) you want to scrape
queries = [
    'cat', 'dog', 'landscape', 'pixel art', 'nature', 
    'architecture', 'city', 'food', 'animals', 'travel',
    'technology', 'art', 'cars', 'mountains', 'beach',
    'waterfalls', 'forest', 'space', 'ocean', 'flowers'
]

# Number of images to fetch per query/category
num_images = 30  # Fetch 50 images per query

# Function to fetch image data from Pixabay API
def fetch_images(query, num_images=50):
    url = f'{BASE_URL}?key={API_KEY}&q={query}&image_type=photo&per_page={num_images}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['hits']
    else:
        print(f"Failed to retrieve data for query '{query}'. Status code: {response.status_code}")
        return []

# Function to download images for each query
def download_images(query, images):
    # Create a folder for the query/category if it doesn't exist
    category_folder = f'images/{query}'
    if not os.path.exists(category_folder):
        os.makedirs(category_folder)

    for i, image in enumerate(images):
        # Get the image URL and the label (description)
        image_url = image['webformatURL']
        label = image.get('tags', 'no-label')

        # Download the image
        img_data = requests.get(image_url).content
        img_filename = f'{query}_{i + 1}.jpg'  # Save with a name like 'cat_1.jpg'
        
        # Save the image to the category folder
        with open(os.path.join(category_folder, img_filename), 'wb') as img_file:
            img_file.write(img_data)
        
        # Optionally, you can save the labels (tags) as metadata in a text file
        with open(os.path.join(category_folder, 'labels.txt'), 'a', encoding='utf-8') as label_file:
            label_file.write(f'{img_filename}: {label}\n')

        print(f"Downloaded {img_filename} for category: {query} with label: {label}")

# Main function to handle multiple categories
def main():
    for query in queries:
        print(f"Fetching images for category: {query}")
        images = fetch_images(query, num_images)
        
        if images:
            # Download the images for the current category
            download_images(query, images)
        else:
            print(f"No images found for category: {query}")

if __name__ == "__main__":
    main()
