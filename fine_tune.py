import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, GPT2LMHeadModel, TrainingArguments, Trainer, DataCollatorForLanguageModeling
import torch
import sys

# load the CSV file
def load_data(csv_path):
    print("loading data...")
    df = pd.read_csv(csv_path).dropna().reset_index(drop=True)
    df = df.head(500)  
    df["text"] = df["caption"] + " <RGB> " + df["rgb_values"].astype(str)
    return Dataset.from_pandas(df[["text"]])

# tokenize the data
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=256)

# initialize model and tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # gpt2 needs this
model = GPT2LMHeadModel.from_pretrained(model_name)

# load and tokenize
data = load_data("C:/Users/korry/Documents/flickr30k_rgb.csv")
tokenized_data = data.map(tokenize_function, batched=True)

# data collator to handle padding
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# training args
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="no",
    per_device_train_batch_size=1,
    num_train_epochs=1,
    weight_decay=0.01,
    save_steps=500,
    save_total_limit=2,
    fp16=False,  # force disable fp16 for cpu
    logging_dir="./logs",
    logging_steps=100,
)

# trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_data,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# train
print("starting fine-tuning...")
trainer.train()
print("fine-tuning complete!")
