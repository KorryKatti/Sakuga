import os
from PIL import Image

def image_to_commands(image_path):
    """
    Converts an image into a sequence of pixel drawing commands.
    Each command is in the format: "draw x,y #hexcolor"
    """
    img = Image.open(image_path)
    pixels = img.load()
    commands = []
    
    # Get image dimensions
    width, height = img.size
    
    # Create drawing commands
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]  # Handle RGB/RGBA
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            commands.append(f"draw {x},{y} {hex_color}")
    
    return ";".join(commands)

def process_images_in_folder(base_dir):
    """
    Loops through all images in the base directory, converts them to commands,
    and saves the commands into a `commands.txt` file in each category folder.
    """
    # Loop through each category folder
    for category in os.listdir(base_dir):
        category_dir = os.path.join(base_dir, category)
        
        # Skip if it's not a directory
        if not os.path.isdir(category_dir):
            continue
        
        print(f"Processing category: {category}")
        
        # Initialize a list to store all commands for this category
        all_commands = []
        
        # Loop through all images in the category folder
        for img_filename in os.listdir(category_dir):
            if img_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                img_path = os.path.join(category_dir, img_filename)
                
                # Convert the image to commands
                commands = image_to_commands(img_path)
                all_commands.append(f"# Image: {img_filename}\n{commands}\n")
        
        # Save all commands to a `commands.txt` file in the category folder
        commands_file = os.path.join(category_dir, "commands.txt")
        with open(commands_file, "w", encoding="utf-8") as f:
            f.write("\n".join(all_commands))
        
        print(f"Saved commands for {category} to {commands_file}")

# Example usage
if __name__ == "__main__":
    base_dir = "images"  # Path to your base directory containing category folders
    process_images_in_folder(base_dir)