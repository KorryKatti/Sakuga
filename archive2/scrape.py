from PIL import Image, ImageDraw
import math
import cv2
import numpy as np
import os
import csv
import requests
from multiprocessing import Pool, cpu_count
from functools import partial
import tqdm
from itertools import product
import time
import random
import json
from urllib.parse import quote

def get_wikimedia_images(query, num_images=30):
    try:
        # Using Wikimedia's official API endpoint
        base_url = "https://commons.wikimedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"{query} filetype:bitmap",
            "srnamespace": "6",  # File namespace
            "srlimit": num_images,
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            image_titles = [item['title'] for item in data.get('query', {}).get('search', [])]
            
            # Get actual image URLs
            image_urls = []
            for title in image_titles:
                img_params = {
                    "action": "query",
                    "format": "json",
                    "prop": "imageinfo",
                    "iiprop": "url",
                    "titles": title
                }
                img_response = requests.get(base_url, params=img_params)
                if img_response.status_code == 200:
                    pages = img_response.json().get('query', {}).get('pages', {})
                    for page in pages.values():
                        if 'imageinfo' in page:
                            image_urls.append(page['imageinfo'][0]['url'])
            
            return image_urls
    except Exception as e:
        print(f"Wikimedia API error for {query}: {e}")
    return []

def get_creative_commons_images(query, num_images=30):
    try:
        # Using CC Search API (no key required)
        base_url = "https://api.creativecommons.engineering/v1/images"
        params = {
            "q": query,
            "page_size": num_images,
            "license": "pdm,cc0",  # Public domain and CC0 licenses
            "format": "json"
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return [result['url'] for result in data.get('results', [])]
    except Exception as e:
        print(f"Creative Commons API error for {query}: {e}")
    return []

def get_images_from_all_sources(query, num_images=30):
    all_urls = []
    
    # Try Wikimedia Commons
    urls = get_wikimedia_images(query, num_images)
    all_urls.extend(urls)
    
    # If we need more images, try Creative Commons
    if len(all_urls) < num_images:
        remaining = num_images - len(all_urls)
        urls = get_creative_commons_images(query, remaining)
        all_urls.extend(urls)
    
    # Remove duplicates while preserving order
    all_urls = list(dict.fromkeys(all_urls))
    
    # Shuffle the results
    random.shuffle(all_urls)
    return all_urls[:num_images]

def process_image(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return []
        
        img = cv2.resize(img, (1024, 1024))
        contrast = np.std(img)
        
        if contrast > 50:
            edges = cv2.Canny(img, 50, 150)
        else:
            edges = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=40, minLineLength=5, maxLineGap=10)
        
        commands = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                thickness = int((255 - img[y1, x1]) / 255 * 5) + 1
                commands.append(f"black {x1} {y1} {x2} {y2} {thickness};")
                
        return commands
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return []

def process_single_image(args):
    category, url_index = args
    try:
        category_dir = os.path.join("dataset", category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Get URLs from free sources
        urls = get_images_from_all_sources(category)
        if not urls or url_index >= len(urls):
            return
        
        url = urls[url_index]
        image_path = os.path.join(category_dir, f"{url_index}.jpg")
        
        # Add delay between requests
        time.sleep(random.uniform(0.5, 1.0))
        
        # Set up headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Download the image
        response = requests.get(url, stream=True, headers=headers)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            # Process the image
            commands = process_image(image_path)
            txt_path = image_path.replace('.jpg', '.txt')
            with open(txt_path, "w") as f:
                f.write("[" + ", ".join(f'"{cmd}"' for cmd in commands) + "]")
            
            return f"Processed {category}/{url_index}"
    except Exception as e:
        print(f"Error processing {category} image {url_index}: {e}")
    return None

def main():
    # Your existing categories list...
    categories = [
    "cat", "dog", "car", "tree", "mountain", "bird", "horse", "bicycle", "ocean", "flower",
    "train", "airplane", "street", "bridge", "city", "sunset", "beach", "forest", "desert", "river",
    "lion", "tiger", "elephant", "zebra", "deer", "house", "castle", "road", "boat", "fire",
    "rain", "snow", "cloud", "moon", "star", "sun", "fish", "butterfly", "lamp", "book",
    "guitar", "piano", "camera", "skyscraper", "bus", "truck", "motorcycle", "soccer", "basketball", "tennis", "chess","anime character", "anime scenery", "manga panel", "cyberpunk", "steampunk",  
    "sci-fi city", "fantasy castle", "mythical creature", "dystopian future", "retro wave",  
    "vaporwave", "glitch art", "dark surrealism", "dreamcore", "liminal space",  
    "digital painting", "low poly art", "pixel art", "mecha", "space nebula",  
    "horror illustration", "eldritch horror", "occult symbols", "psychedelic art", "abstract expressionism",  
    "nude art", "life drawing", "tattoo design", "gothic architecture", "street graffiti",  
    "medieval armor", "japanese ukiyo-e", "futuristic fashion", "traditional ink drawing", "surreal portrait",  
    "chiaroscuro painting", "cybernetic implants", "AI-generated art", "hyperrealism", "anime girl aesthetic",  
    "demon girl", "angelic warrior", "robotic humanoid", "dark fantasy", "Lovecraftian horror",  
    "warrior monk", "mythological gods", "retro anime", "vintage horror poster", "baroque painting"

]
    
    images_per_category = 30
    
    # Create all possible combinations of categories and image indices
    tasks = list(product(categories, range(images_per_category)))
    
    # Create the base directory
    os.makedirs("dataset", exist_ok=True)
    
    # Process all images in parallel using a single pool
    with Pool(processes=cpu_count()) as pool:
        list(tqdm.tqdm(
            pool.imap_unordered(process_single_image, tasks),
            total=len(tasks),
            desc="Processing images"
        ))
    
    print("Dataset generation complete.")

if __name__ == "__main__":
    main()