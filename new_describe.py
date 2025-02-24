# use if new categories added and to avoid re describigimport os
import os
import torch
import json
from PIL import Image
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from tqdm import tqdm

def describe_image(category, index, model, processor, tokenizer, device):
    try:
        img_path = f"dataset/{category}/{index}.jpg"
        txt_path = f"dataset/{category}/{index}.txt"
        desc_path = f"dataset/{category}/{index}_desc.txt"
        
        if not os.path.exists(img_path) or not os.path.exists(txt_path) or os.path.exists(desc_path):
            return None  # Skip if description already exists or required files are missing
        
        image = Image.open(img_path).convert("RGB")
        pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
        
        output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
        description = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        with open(desc_path, "w") as f:
            json.dump({"description": description, "commands": open(txt_path).read()}, f, indent=4)
        
        return f"Processed {category}/{index}"
    except Exception as e:
        return f"Error processing {category}/{index}: {e}"

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name = "nlpconnect/vit-gpt2-image-captioning"
    
    model = VisionEncoderDecoderModel.from_pretrained(model_name).to(device)
    processor = ViTImageProcessor.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    categories = os.listdir("dataset")
    images_per_category = 30  # Adjust if needed
    tasks = [(cat, idx) for cat in categories for idx in range(images_per_category)]
    
    for category, index in tqdm(tasks, total=len(tasks)):
        result = describe_image(category, index, model, processor, tokenizer, device)
        if result:
            print(result)
    
    print("Image description complete.")

if __name__ == "__main__":
    main()
