import os

def clean_labels(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    for line in lines:
        # Extract the labels from the line
        img_filename, labels = line.split(':', 1)
        
        # Clean the labels: remove duplicates, make lowercase, and strip whitespace
        label_list = labels.split(',')
        cleaned_labels = list(set([label.strip().lower() for label in label_list]))
        
        # Rebuild the cleaned line
        cleaned_line = f'{img_filename}: {", ".join(sorted(cleaned_labels))}\n'
        cleaned_lines.append(cleaned_line)
    
    # Write the cleaned labels back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

# Path to the directory containing your label files
categories = [
    'cat', 'dog', 'landscape', 'pixel art', 'nature', 
    'architecture', 'city', 'food', 'animals', 'travel',
    'technology', 'art', 'cars', 'mountains', 'beach',
    'waterfalls', 'forest', 'space', 'ocean', 'flowers'
]  # Update with all your categories

for category in categories:
    file_path = os.path.join('images',category, 'labels.txt')
    clean_labels(file_path)

print("Labels cleaned successfully!")
