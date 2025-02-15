import os
import json

def create_dataset(base_dir):
    """
    Creates a dataset by pairing text prompts from `labels.txt` with commands from `commands.txt`.
    Saves the dataset as a JSON file.
    """
    dataset = []
    
    # Loop through each category folder
    for category in os.listdir(base_dir):
        category_dir = os.path.join(base_dir, category)
        
        # Skip if it's not a directory
        if not os.path.isdir(category_dir):
            continue
        
        print(f"Processing category: {category}")
        
        # Path to the labels and commands files
        labels_file = os.path.join(category_dir, "labels.txt")
        commands_file = os.path.join(category_dir, "commands.txt")
        
        # Skip if either file is missing
        if not (os.path.exists(labels_file) and os.path.exists(commands_file)):
            print(f"Skipping {category}: Missing labels.txt or commands.txt")
            continue
        
        # Read labels and commands
        with open(labels_file, "r", encoding="utf-8") as f:
            labels = f.readlines()
        
        with open(commands_file, "r", encoding="utf-8") as f:
            commands = f.read().split("# Image:")[1:]  # Split by image
        
        # Pair each label with its corresponding commands
        for label, cmd_block in zip(labels, commands):
            cmd_lines = cmd_block.split("\n", 1)
            if len(cmd_lines) < 2:
                continue  # Skip if command block format is incorrect
            
            img_filename, cmd_data = cmd_lines
            img_filename = img_filename.strip()
            cmd_data = cmd_data.strip()
            
            # Add to dataset
            dataset.append({
                "prompt": label.split(":", 1)[1].strip(),  # Extract the label text
                "commands": cmd_data
            })
    
    # Save the dataset to a JSON file
    dataset_file = os.path.join(base_dir, "dataset.json")
    with open(dataset_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
    
    print(f"Dataset saved to {dataset_file}")

# Example usage
if __name__ == "__main__":
    base_dir = "images"  # Path to your base directory containing category folders
    create_dataset(base_dir)
