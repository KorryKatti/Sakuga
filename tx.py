import numpy as np
from PIL import Image
import csv

# read csv and grab row 7, col 2 (0-indexed)
with open("dataset.csv", newline='') as f:
    reader = csv.reader(f)
    rows = list(reader)
    rgb_text = rows[302][1]  # row 7, column 2

print("raw csv rgb string:")
print(rgb_text[:300] + '...')  # just a preview

# convert CSV-style string to list of ints
try:
    rgb_numbers = list(map(int, rgb_text.strip().split(',')))
except Exception as e:
    print("failed to parse ints:", e)
    exit()

# reshape to 96x96x3
try:
    img_array = np.array(rgb_numbers, dtype=np.uint8).reshape((48, 48, 3))
except ValueError as e:
    print("reshape error:", e)
    print(f"length of list = {len(rgb_numbers)}, expected 96*96*3 = 27648")
    exit()

# display + save original image
img = Image.fromarray(img_array, "RGB")
img.show()
img.save("generated_from_csv.png")

# upscale to 128x128
img_128 = img.resize((128, 128), resample=Image.Resampling.LANCZOS)
img_128.show()
img_128.save("generated_from_csv_128x128.png")

# upscale to 512x512
img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
img_512.show()
img_512.save("generated_from_csv_512x512.png")
