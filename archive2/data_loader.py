import os
import json
from transformers import BertTokenizer
from renderer import render

# Initialize the tokenizer
TOKENIZER = BertTokenizer.from_pretrained('bert-base-uncased')

# Function to load and preprocess data
def load_data(dataset_path):
    descriptions = []
    images = []
    
    # Iterate over each directory in the dataset
    for category in os.listdir(dataset_path):
        category_path = os.path.join(dataset_path, category)
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                if file.endswith('_desc.txt'):
                    desc_path = os.path.join(category_path, file)
                    with open(desc_path, 'r') as f:
                        data = json.load(f)
                        description = data['description']
                        commands = json.loads(data['commands'])
                        
                        # Tokenize the description
                        tokenized_desc = TOKENIZER(description, return_tensors='pt')
                        descriptions.append(tokenized_desc)
                        
                        # Generate image from commands
                        #render(commands)
                        #images.append('output.png')  # Assuming render saves the image as output.png
    
    return descriptions, images

# Example usage
if __name__ == "__main__":
    dataset_path = 'dataset/'  # Path to the dataset
    descriptions, images = load_data(dataset_path)
    print(f"Loaded {len(descriptions)} descriptions and {len(images)} images.") 