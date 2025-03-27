"""
RoboEyes Python Demo
Demonstrates the RoboEyes Python implementation
"""

import pygame
import sys
import time
from robo_eyes import RoboEyes
from moods_utils import DEFAULT, TIRED, SAD, EXCITED
from shapes_utils import N, NE, E, SE, S, SW, W, NW

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
    
    # Store default values for reset
    eyes.eye_l_width_default = 80
    eyes.eye_r_width_default = 80
    eyes.eye_l_height_default = 80
    eyes.eye_r_height_default = 80
    
    # Set default mood
    eyes.set_mood(DEFAULT)
    
    # Set curiosity effect
    eyes.set_curiosity(True)
    
    # Set initial eye shape
    eyes.set_eye_shape("pill")
    
    # Main loop
    try:
        
        # Display instructions
        print("RoboEyes Python Demo")
        print("--------------------")
        print("Press ESC or close the window to exit")
        print("Press 1-4 to change mood:")
        print("  1: DEFAULT, 2: TIRED, 3: SAD, 4: EXCITED")
        print("Press B to blink")
        print("Press L to laugh")
        print("Press F to look confused")
        print("Press E to look excited")
        print("Use ARROW KEYS to move eyes (auto-centers after 5 seconds of inactivity)")
        print("Press W to wink left eye")
        print("Press Q to wink right eye")
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
                        eyes.set_mood(SAD)
                        print("Mood: SAD")
                    elif event.key == pygame.K_4:
                        eyes.set_mood(EXCITED)
                        print("Mood: EXCITED")
                    elif event.key == pygame.K_b:
                        eyes.blink()
                        print("Blinking")
                    elif event.key == pygame.K_l:
                        eyes.anim_laugh()
                        print("Laughing")
                    elif event.key == pygame.K_f:
                        eyes.anim_confused()
                        print("Confused")
                    elif event.key == pygame.K_e:
                        eyes.anim_excited()
                        print("Excited")
                    elif event.key == pygame.K_w:
                        eyes.wink(left_eye=True)
                        print("Winking left eye")
                    elif event.key == pygame.K_q:
                        eyes.wink(left_eye=False)
                        print("Winking right eye")
                    elif event.key == pygame.K_SPACE:
                        # Reset to default
                        eyes.set_mood(DEFAULT)
                        eyes.set_position(DEFAULT)
                        eyes.set_h_flicker(False)
                        eyes.set_v_flicker(False)
                        print("Reset to default")
            

            
            # Update the eyes
            eyes.update()
    
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        eyes.quit()

if __name__ == "__main__":
    main()
