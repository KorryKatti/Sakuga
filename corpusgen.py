import os
import json

data_directory = "dataset"  # change if needed
output_file = "corpus.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for category in os.listdir(data_directory):
        category_path = os.path.join(data_directory, category)
        if not os.path.isdir(category_path):
            continue  # skip non-folder files
        
        for filename in os.listdir(category_path):
            if filename.endswith("_desc.txt"):
                desc_path = os.path.join(category_path, filename)
                with open(desc_path, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)
                    description = data.get("description", "").strip()
                    if description:
                        f.write(description + "\n")

print(f"Corpus created at {output_file}")
