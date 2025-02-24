# Step 4: Train the AI Model
import random
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments
from datasets import Dataset
import torch

# Step 4.1: Synthetic Data Generation
def generate_synthetic_data(num_samples=1000):
    data = []
    colors = {
        "sky": ["#87CEEB", "#FFA500", "#FF4500"],
        "sand": ["#F4A460", "#DEB887", "#CD853F"],
        "sun": ["#FFFF00", "#FFD700", "#FFA500"],
        "ocean": ["#0000FF", "#4682B4", "#1E90FF"],
        "text": ["#000000", "#FFFFFF"]
    }

    for _ in range(num_samples):
        # Randomly generate a scene type (beach, sunset, etc.)
        scene_type = random.choice(["beach", "sunset", "forest"])

        # Generate DSL commands based on scene type
        commands = []
        if scene_type == "beach":
            commands.append(f"set_bg {random.choice(colors['sky'])};")
            commands.append(f"fill_rect 0,50,100,100 {random.choice(colors['sand'])};")
            commands.append(f"draw_circle {random.randint(70,90)},{random.randint(10,30)},15 {random.choice(colors['sun'])};")
            for y in [55, 60, 65]:
                commands.append(f"draw_line 0,{y},100,{y} {random.choice(colors['ocean'])};")

        elif scene_type == "sunset":
            commands.append(f"fill_gradient 0,0,100,50 {random.choice(colors['sky'])},#FF4500;")
            commands.append(f"draw_circle 50,20,10 {random.choice(colors['sun'])};")

        # Generate a text prompt describing the scene
        text_prompt = f"A {scene_type} scene with {random.choice(['bright', 'calm', 'vivid'])} colors."

        data.append({
            "text": text_prompt,
            "commands": " ".join(commands)
        })

    return data

# Step 4.2: Model Setup and Training
def train_model():
    # Generate synthetic data
    synthetic_data = generate_synthetic_data(1000)

    # Convert synthetic data to a Hugging Face Dataset
    dataset = Dataset.from_dict({
        "text": [d["text"] for d in synthetic_data],
        "commands": [d["commands"] for d in synthetic_data]
    })

    # Split into train/test
    dataset = dataset.train_test_split(test_size=0.1)

    # Load tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    model = T5ForConditionalGeneration.from_pretrained("t5-small")

    # Tokenize the dataset
    def tokenize_function(examples):
        model_inputs = tokenizer(
            ["generate commands: " + text for text in examples["text"]],
            max_length=128,
            padding="max_length",
            truncation=True
        )
        
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(
                examples["commands"],
                max_length=256,
                padding="max_length",
                truncation=True
            )

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = dataset.map(tokenize_function, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=3e-4,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=10,
        weight_decay=0.01,
        save_total_limit=3,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
    )

    # Start training
    trainer.train()

    # Save the model and tokenizer
    model.save_pretrained("./t5-dsl-generator")
    tokenizer.save_pretrained("./t5-dsl-generator")

# Step 4.3: Generate Commands with the Trained Model
def generate_commands(text_prompt, model_path="./t5-dsl-generator"):
    # Load the trained model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # Prepare input
    input_text = "generate commands: " + text_prompt
    inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True)
    
    # Generate commands
    outputs = model.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=256,
        num_beams=5,
        early_stopping=True
    )
    
    # Decode and return the commands
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Step 4.4: Full Integration Pipeline
if __name__ == "__main__":
    # Step 1: Train the model (only need to do this once)
    print("Training the model...")
    train_model()
    print("Model trained and saved!")

    # Step 2: Generate commands from a text prompt
    text_prompt = "A beach with golden sand and a bright sun"
    print(f"Generating commands for: {text_prompt}")
    commands = generate_commands(text_prompt)
    print("Generated Commands:")
    print(commands)

    # Step 3: Parse and render the commands
    from renderer import CommandParser, Renderer  # Import your renderer and parser

    parser = CommandParser()
    renderer = Renderer(width=100, height=100)

    try:
        parsed_commands = parser.parse(commands)
        renderer.execute_commands(parsed_commands)
        renderer.show_image()
    except ValueError as e:
        print(f"Error: {e}")