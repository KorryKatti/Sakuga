import streamlit as st
from renderer import CommandParser, Renderer
from train_ai_model import generate_commands

# Streamlit app
st.title("AI Image Generator")
st.write("Enter a text prompt and see the generated image!")

# User input
text_prompt = st.text_input("Enter a prompt (e.g., 'A beach with golden sand and a bright sun'):")

if text_prompt:
    # Generate commands
    commands = generate_commands(text_prompt)
    st.write("Generated Commands:")
    st.code(commands)

    # Parse and render the commands
    parser = CommandParser()
    renderer = Renderer(width=100, height=100)

    try:
        parsed_commands = parser.parse(commands)
        renderer.execute_commands(parsed_commands)
        renderer.save_image("output.png")
        st.image("output.png", caption="Generated Image", use_column_width=True)
    except ValueError as e:
        st.error(f"Error: {e}")