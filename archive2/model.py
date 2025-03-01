import torch
import torch.nn as nn
from transformers import BertModel

class TextToImageModel(nn.Module):
    def __init__(self):
        super(TextToImageModel, self).__init__()
        # Load pre-trained BERT model
        self.text_encoder = BertModel.from_pretrained('bert-base-uncased')
        
        # Define a simple image generator
        self.image_generator = nn.Sequential(
            nn.Linear(self.text_encoder.config.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512 * 512 * 3),  # Assuming output image size is 512x512 with 3 color channels
            nn.Sigmoid()  # To ensure pixel values are between 0 and 1
        )

    def forward(self, input_ids, attention_mask):
        # Encode text
        text_features = self.text_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        # Use the [CLS] token representation
        cls_features = text_features[:, 0, :]
        # Generate image
        generated_image = self.image_generator(cls_features)
        # Reshape to image dimensions
        generated_image = generated_image.view(-1, 3, 512, 512)
        return generated_image

# Example usage
if __name__ == "__main__":
    model = TextToImageModel()
    print(model) 