import os
import torch
import json
import tqdm
from PIL import Image
from multiprocessing import Pool, cpu_count, Manager
from transformers import LlavaForConditionalGeneration, LlavaProcessor

def init_worker(model_name, device, shared_dict):
    global model, processor
    model = LlavaForConditionalGeneration.from_pretrained(model_name).to(device)
    processor = LlavaProcessor.from_pretrained(model_name)
    shared_dict['device'] = device

def describe_image(args):
    category, index = args
    try:
        img_path = f"dataset/{category}/{index}.jpg"
        txt_path = f"dataset/{category}/{index}.txt"
        desc_path = f"dataset/{category}/{index}_desc.txt"
        
        if not os.path.exists(img_path) or not os.path.exists(txt_path):
            return None
        
        image = Image.open(img_path).convert("RGB")
        inputs = processor(images=image, text="Describe this image:", return_tensors="pt").to(model.device)
        output = model.generate(**inputs, max_new_tokens=100)
        description = processor.tokenizer.decode(output[0], skip_special_tokens=True)
        
        with open(desc_path, "w") as f:
            json.dump({"description": description, "commands": open(txt_path).read()}, f, indent=4)
        
        return f"Processed {category}/{index}"
    except Exception as e:
        return f"Error processing {category}/{index}: {e}"

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_name = "liuhaotian/llava-v1.5-7b"
    
    categories = os.listdir("dataset")
    images_per_category = 30  # Adjust if needed
    tasks = [(cat, idx) for cat in categories for idx in range(images_per_category)]
    
    with Manager() as manager:
        shared_dict = manager.dict()
        with Pool(processes=cpu_count(), initializer=init_worker, initargs=(model_name, device, shared_dict)) as pool:
            for result in tqdm.tqdm(pool.imap_unordered(describe_image, tasks), total=len(tasks)):
                if result:
                    print(result)
    
    print("Image description complete.")

if __name__ == "__main__":
    main()
