import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
import torch
import os
HF_HUB_ENABLE_HF_TRANSFER=1
# Load Hugging Face token from environment variable
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("Hugging Face token not found. Please set the 'HF_TOKEN' environment variable.")

# load the CSV file
def load_data(csv_path, limit=300):  # trimmed size to reduce RAM spikes
    print("loading data...")
    df = pd.read_csv(csv_path).dropna().reset_index(drop=True)
    df = df.head(limit)
    df["text"] = df["caption"] + " <RGB> " + df["rgb_values"].astype(str)
    return Dataset.from_pandas(df[["text"]])

# tokenize the data
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=1024)

# lightweight model for CPUs
model_name = "mistralai/Mistral-7B-Instruct-v0.1"  # or use a small distilled model if even this breaks
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)

# load and tokenize
data = load_data("C:\\Users\\korry\\Documents\\flickr30k_rgb_96.csv")
tokenized_data = data.map(tokenize_function, batched=True)

# data collator to handle padding
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# training args
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="no",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,  # more virtual batch, even safer
    num_train_epochs=2,  # 1 was short
    weight_decay=0.01,
    save_steps=999999,  # no I/O interruption
    logging_dir="./logs",
    logging_steps=20,
    remove_unused_columns=True,
    fp16=False,
    bf16=False,
    dataloader_num_workers=0,
    optim="adamw_torch",
    push_to_hub=False,
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

# save model + tokenizer
trainer.save_model("./results")
tokenizer.save_pretrained("./results")
print("model saved!")
