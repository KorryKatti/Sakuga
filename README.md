# Sakuga
my attempt at making an ai image generator

#### how to run
1. download zip
2. pip install -r requirements.txt
3. python cli_app.py "A beach with golden sand" --width 200 --height 200 --output beach.png --show

#### Command-Line Arguments:
Flag	Description	Default
--width	Image width	100
--height	Image height	100
--output	Output filename	output.png
--show	Display the image	False

<!--future plans
How to Improve Image Quality
1. Expand the Training Dataset
Add more scene types (e.g., forests, cities, abstract art).

Use real-world data by collecting prompts from users and manually creating DSL commands.

Use procedural generation tools like Blender to create complex scenes.

2. Enhance the DSL
Add gradients:

plaintext
Copy
fill_gradient 0,0,100,50 #FF0000,#00FF00;
Add textures:

plaintext
Copy
fill_texture 0,0,100,100 "wave_pattern";
Add layers and groups:

plaintext
Copy
begin_layer "background";
set_bg #87CEEB;
end_layer;
3. Improve the AI Model
Use larger models like t5-base or gpt-3.

Fine-tune the model on a GPU for faster training.

Use beam search for better command coherence:

python
Copy
outputs = model.generate(..., num_beams=10, early_stopping=True)
4. Add Error Handling
Validate commands to ensure they are within canvas bounds.

Use fallback rendering for invalid commands (e.g., replace with a default shape/color).

5. Optimize Rendering
Use anti-aliasing to smooth edges for circles and lines:

python
Copy
self.draw.line(..., width=2, joint="curve")
Increase the default canvas size to 512x512 for higher resolution.

6. User Feedback Loop
Allow users to correct bad outputs and save corrections to a dataset.

Retrain the model periodically with new data.

Example Workflow
Generate a beach scene:

bash
Copy
python cli_app.py "A beach with golden sand" --width 200 --height 200 --output beach.png --show
Improve the dataset by adding more scenes and retraining the model.

Enhance the DSL to support gradients and textures.

Fine-tune the model on a GPU for better performance.




>
