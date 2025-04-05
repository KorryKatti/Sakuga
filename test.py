import torch
from transformers import GPT2LMHeadModel, AutoTokenizer
import numpy as np
from PIL import Image
import re

# load model + tokenizer
model_path = "./results"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token
model.eval()

# get prompt
prompt = input("caption > ")
input_ids = tokenizer.encode(prompt + " <RGB>", return_tensors="pt")
attention_mask = (input_ids != tokenizer.pad_token_id).long()

# generate safely
with torch.no_grad():
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_new_tokens=800,  # enough for 128x128x3
        do_sample=True,
        temperature=0.8,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id,
    )

# decode and clean
decoded = tokenizer.decode(output[0])
rgb_text = decoded.split("<RGB>")[-1]
rgb_numbers = list(map(int, re.findall(r'\d+', rgb_text)))

# reshape
try:
    img_array = np.array(rgb_numbers, dtype=np.uint8).reshape((128, 128, 3))
except ValueError:
    print("bad RGB data. model probably hallucinated.")
    exit()

# show/save
img = Image.fromarray(img_array, "RGB")
img.show()
img.save("generated.png")
