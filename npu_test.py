from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# load model + tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# dummy input
dummy_input = tokenizer("describe a sunset", return_tensors="pt")

# export to ONNX
torch.onnx.export(
    model,
    (dummy_input["input_ids"]),
    "gpt2.onnx",
    input_names=["input_ids"],
    output_names=["logits"],
    dynamic_axes={"input_ids": {0: "batch_size", 1: "sequence"}},
    opset_version=13
)

print("exported ✅")
