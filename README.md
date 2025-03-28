# Ani-eyes GPT

A Python project that aims to mimic the expressive eyes from Pixar characters and Cosmo robots. We're creating animated, expressive eyes that can convey emotion and personality using Pygame. We plan to add a Large Language Model (LLM) to drive the expressions based on context and interaction.

## Features

- Customizable eye shapes (width, height, border radius, spacing)
- Multiple mood expressions (default, tired, angry, happy)
- Various animations (blinking, laughing, confused)
- Automatic behaviors (auto-blinker, idle mode)
- Smooth transitions between states
- Cyclops mode (single eye)
- Curiosity effect

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/Ani-eyes-GPT.git
cd Ani-eyes-GPT
```

2. Create a virtual environment (recommended):
```
python -m venv env
```

3. Activate the virtual environment:
   - On macOS/Linux:
   ```
   source env/bin/activate
   ```
   - On Windows:
   ```
   env\Scripts\activate
   ```

4. Install the required dependencies:

   **For macOS (especially newer Python versions like 3.13+):**
   ```
   pip install pygame --pre
   ```
   If you encounter build errors with the above command, try:
   ```
   brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf portmidi
   pip install pygame --pre
   ```

   **For older Python versions or other OS:**
   ```
   pip install -r requirements.txt
   ```

   **Note for Windows users:**
   If you encounter issues, try installing the pre-built wheel from:
   https://www.pygame.org/wiki/GettingStarted

   **Note for Linux users:**
   You may need to install additional dependencies:
   ```
   sudo apt-get install python3-pygame
   ```
   Or for the required SDL libraries:
   ```
   sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   ```

## Usage

Run the demo:
```
python main.py
```

### Controls

- **ESC**: Exit the application
- **1-4**: Change mood (1=Default, 2=Tired, 3=Angry, 4=Happy)
- **C**: Toggle cyclops mode
- **B**: Trigger blink animation
- **L**: Trigger laugh animation
- **F**: Trigger confused animation
- **SPACE**: Reset to default settings

## Creating Your Own Animations

You can create your own animations by using the RoboEyes class in your code:

```python
from robo_eyes import RoboEyes

# Create and initialize RoboEyes
eyes = RoboEyes()
eyes.begin(640, 320, 60)  # width, height, fps

# Configure eye properties
eyes.set_width(80, 80)
eyes.set_height(80, 80)
eyes.set_border_radius(20, 20)
eyes.set_space_between(40)

# Set mood
eyes.set_mood(HAPPY)

# Main loop
while eyes.is_running():
    eyes.update()
```

## Future Integration with LLMs

This project is designed to connect with Large Language Models to create more interactive and responsive eye animations based on conversation or other inputs. The goal is to have the eyes express emotions and reactions that align with the context of interactions, similar to how Pixar characters and Cosmo robots convey personality through their eye movements and expressions.

## Credits

- Inspired by Pixar character animations and Cosmo robot expressions
- Original Arduino library by [FluxGarage](https://github.com/FluxGarage/RoboEyes)
- Python implementation created as a standalone version with plans for LLM integration
