"""
RoboEyes Python Demo
Demonstrates the RoboEyes Python implementation
"""

import pygame
import sys
import time
from robo_eyes import RoboEyes, DEFAULT, TIRED, ANGRY, HAPPY, N, NE, E, SE, S, SW, W, NW

def main():
    # Create RoboEyes instance
    eyes = RoboEyes()
    
    # Initialize with screen dimensions and frame rate
    screen_width = 640
    screen_height = 320
    max_fps = 60
    
    if not eyes.begin(screen_width, screen_height, max_fps):
        print("Failed to initialize RoboEyes")
        return
    
    # Configure eye properties
    eyes.set_width(80, 80)
    eyes.set_height(80, 80)
    eyes.set_border_radius(20, 20)
    eyes.set_space_between(40)
    
    # Enable auto blinker and idle mode
    eyes.set_auto_blinker(True, 3, 2)
    eyes.set_idle_mode(True, 4, 2)
    
    # Set curiosity effect
    eyes.set_curiosity(True)
    
    # Main loop
    try:
        current_mood = DEFAULT
        moods = [DEFAULT, TIRED, ANGRY, HAPPY]
        mood_names = ["DEFAULT", "TIRED", "ANGRY", "HAPPY"]
        mood_change_time = time.time()
        mood_duration = 5  # seconds
        
        cyclops_mode = False
        cyclops_change_time = time.time()
        cyclops_duration = 15  # seconds
        
        # Display instructions
        print("RoboEyes Python Demo")
        print("--------------------")
        print("Press ESC or close the window to exit")
        print("Press 1-4 to change mood")
        print("Press C to toggle cyclops mode")
        print("Press B to blink")
        print("Press L to laugh")
        print("Press F to look confused")
        print("Press SPACE to reset to default")
        
        while eyes.is_running():
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    eyes.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        eyes.quit()
                        return
                    elif event.key == pygame.K_1:
                        eyes.set_mood(DEFAULT)
                        print("Mood: DEFAULT")
                    elif event.key == pygame.K_2:
                        eyes.set_mood(TIRED)
                        print("Mood: TIRED")
                    elif event.key == pygame.K_3:
                        eyes.set_mood(ANGRY)
                        print("Mood: ANGRY")
                    elif event.key == pygame.K_4:
                        eyes.set_mood(HAPPY)
                        print("Mood: HAPPY")
                    elif event.key == pygame.K_c:
                        cyclops_mode = not cyclops_mode
                        eyes.set_cyclops(cyclops_mode)
                        print(f"Cyclops mode: {'ON' if cyclops_mode else 'OFF'}")
                    elif event.key == pygame.K_b:
                        eyes.blink()
                        print("Blinking")
                    elif event.key == pygame.K_l:
                        eyes.anim_laugh()
                        print("Laughing")
                    elif event.key == pygame.K_f:
                        eyes.anim_confused()
                        print("Confused")
                    elif event.key == pygame.K_SPACE:
                        # Reset to default
                        eyes.set_mood(DEFAULT)
                        eyes.set_cyclops(False)
                        eyes.set_position(DEFAULT)
                        eyes.set_h_flicker(False)
                        eyes.set_v_flicker(False)
                        print("Reset to default")
            
            # Auto change mood for demo purposes
            current_time = time.time()
            if current_time - mood_change_time > mood_duration:
                current_mood = (current_mood + 1) % len(moods)
                eyes.set_mood(moods[current_mood])
                print(f"Auto changing mood to: {mood_names[current_mood]}")
                mood_change_time = current_time
            
            # Update the eyes
            eyes.update()
    
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        eyes.quit()

if __name__ == "__main__":
    main()
