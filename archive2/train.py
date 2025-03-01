import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from data_loader import load_data
from model import TextToImageModel
from renderer import render
from PIL import Image
import numpy as np

# Load data
print("Loading data...")
descriptions, commands_list = load_data('dataset/')

# Generate images from commands and convert to tensors
image_tensors = []
for commands in commands_list:
    render(commands)  # Generate image using renderer
    img = Image.open('output.png')
    img_array = np.array(img) / 255.0  # Normalize pixel values
    image_tensors.append(torch.tensor(img_array).permute(2, 0, 1).float())  # Convert to tensor and permute dimensions

# Create a dataset and dataloader
train_dataset = TensorDataset(torch.stack([desc['input_ids'].squeeze() for desc in descriptions]),
                              torch.stack([desc['attention_mask'].squeeze() for desc in descriptions]),
                              torch.stack(image_tensors))
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

# Initialize model, loss function, and optimizer
model = TextToImageModel()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
def train_model(num_epochs=10):
    model.train()
    for epoch in range(num_epochs):
        running_loss = 0.0
        for input_ids, attention_mask, target_images in train_loader:
            optimizer.zero_grad()
            # Forward pass
            outputs = model(input_ids, attention_mask)
            # Compute loss
            loss = criterion(outputs, target_images)
            # Backward pass and optimization
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}")

# Run training
if __name__ == "__main__":
    train_model() 