"""
RoboEyes Python Demo
Demonstrates the RoboEyes Python implementation
"""

import pygame
import sys
import time
from robo_eyes import RoboEyes, DEFAULT, TIRED, EXCITED, N, NE, E, SE, S, SW, W, NW

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
    
    # Enable auto blinker and idle mode
    eyes.set_auto_blinker(True, 3, 2)
    eyes.set_idle_mode(True, 4, 2)
    
    # Set curiosity effect
    eyes.set_curiosity(True)
    
    # Set initial eye shape
    eyes.set_eye_shape("pill")
    
    # Main loop
    try:
        current_mood = DEFAULT
        moods = [DEFAULT, TIRED, EXCITED]
        mood_names = ["DEFAULT", "TIRED", "EXCITED"]
        mood_change_time = time.time()
        mood_duration = 5  # seconds
        
        # Manual control flag
        manual_control = False
        
        # Display instructions
        print("RoboEyes Python Demo")
        print("--------------------")
        print("Press ESC or close the window to exit")
        print("Press 1-3 to change mood:")
        print("  1: DEFAULT, 2: TIRED, 3: EXCITED")
        print("Press B to blink")
        print("Press L to laugh")
        print("Press F to look confused")
        print("Press E to look excited")
        print("Press M to toggle manual control with arrow keys")
        print("Use ARROW KEYS to move eyes when in manual control mode")
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
                    elif event.key == pygame.K_m:
                        manual_control = not manual_control
                        eyes.set_manual_control(manual_control)
                        print(f"Manual control with arrow keys: {'ON' if manual_control else 'OFF'}")
                    elif event.key == pygame.K_SPACE:
                        # Reset to default
                        eyes.set_mood(DEFAULT)
                        eyes.set_position(DEFAULT)
                        eyes.set_h_flicker(False)
                        eyes.set_v_flicker(False)
                        eyes.set_manual_control(False)
                        manual_control = False
                        print("Reset to default")
            
            # Auto change mood for demo purposes (only if not in manual control)
            if not manual_control:
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
