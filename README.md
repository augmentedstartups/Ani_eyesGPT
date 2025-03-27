# RoboEyes Python

A Python implementation of the FluxGarage RoboEyes library, originally designed for Arduino. This version creates animated robot eyes in a window using Pygame.

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
git clone https://github.com/yourusername/project_eyes.git
cd project_eyes
```

2. Install the required dependencies:
```
pip install -r requirements.txt
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

This project is designed to eventually connect with Large Language Models to create more interactive and responsive eye animations based on conversation or other inputs.

## Credits

- Original Arduino library by [FluxGarage](https://github.com/FluxGarage/RoboEyes)
- Python implementation created as a standalone version
