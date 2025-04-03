from datasets import load_dataset

dataset = load_dataset("nlphuji/flickr30k")
print(dataset)
image = dataset["test"][100]["image"]
text = dataset["test"][100]["caption"]
image.show()
print(text)