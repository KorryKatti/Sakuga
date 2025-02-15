import json

with open("images/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)
print(f"Dataset length: {len(dataset)}")
print(f"First item: {dataset[0]}")