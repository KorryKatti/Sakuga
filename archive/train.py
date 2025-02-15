import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the dataset with progress bar
logger.info("Loading dataset...")
with open("images/dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)
logger.info(f"Loaded {len(dataset)} examples")

# Convert to HF Dataset with a smaller subset first for testing
logger.info("Converting to HuggingFace Dataset format...")
SUBSET_SIZE = 1000  # Start with a smaller subset for testing
test_dataset = dataset[:SUBSET_SIZE]
hf_dataset = Dataset.from_dict({
    "prompt": [item["prompt"] for item in test_dataset],
    "commands": [item["commands"] for item in test_dataset]
})

# Load model with logging
logger.info("Loading T5 model and tokenizer...")
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Modified preprocessing function with smaller chunks
def preprocess_function(examples):
    logger.info(f"Processing batch of {len(examples['prompt'])} examples")
    inputs = [f"translate text to commands: {prompt}" for prompt in examples["prompt"]]
    targets = examples["commands"]
    
    model_inputs = tokenizer(
        inputs, 
        max_length=512, 
        truncation=True, 
        padding="max_length",
        return_tensors="pt"
    )
    
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets, 
            max_length=512, 
            truncation=True, 
            padding="max_length",
            return_tensors="pt"
        )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Process the dataset with smaller batches and progress bar
logger.info("Tokenizing dataset...")
tokenized_dataset = hf_dataset.map(
    preprocess_function,
    batched=True,
    batch_size=16,  # Smaller batch size
    num_proc=8,     # Single process for debugging
    remove_columns=hf_dataset.column_names,
    desc="Tokenizing"
)

logger.info("Splitting dataset...")
train_test_split = tokenized_dataset.train_test_split(test_size=0.1)
train_dataset = train_test_split["train"]
eval_dataset = train_test_split["test"]

# Modified training arguments for better memory management
logger.info("Setting up training arguments...")
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
    save_steps=500,
    logging_dir="./logs",
    logging_steps=10,
    gradient_accumulation_steps=4,  # Added this to help with memory
    fp16=True,  # Added this to help with memory
)

# Initialize and train
logger.info("Initializing trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
)

logger.info("Starting training...")
trainer.train()

# Save the model
logger.info("Saving model...")
model.save_pretrained("./text_to_commands_model")
tokenizer.save_pretrained("./text_to_commands_model")
logger.info("Model saved to ./text_to_commands_model")