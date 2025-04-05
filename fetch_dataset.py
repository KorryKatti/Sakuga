from datasets import load_dataset

dataset = load_dataset("jxie/flickr8k")
print(dataset["test"].features)
