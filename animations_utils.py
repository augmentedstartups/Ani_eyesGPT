"""
Animations utilities for RoboEyes
Handles all animation-related functionality including blinking, winking, 
laughing, confused animations, and idle mode.
"""

import random
import time
import math
import pygame

class AnimationsHandler:
    def __init__(self, parent):
        """Initialize animations with reference to parent RoboEyes object"""
        self.parent = parent
        
        # Animation state flags
        self.is_blinking = False
        self.is_winking = False
        self.blink_start_time = 0
        self.blink_duration = 0.3  # seconds
        self.wink_left_eye = True  # Which eye to wink
        
        self.is_laughing = False
        self.laugh_start_time = 0
        self.laugh_duration = 1.0  # seconds
        
        self.is_confused = False
        self.confused_start_time = 0
        self.confused_duration = 1.0  # seconds
        
        # Auto animations
        self.auto_blinker = True
        self.auto_blinker_interval = 3  # Minimum 3 seconds as mentioned in the video
        self.auto_blinker_variation = 2  # Random variation 0-2 seconds as mentioned in the video
        self.auto_blinker_last_time = time.time()
        
        self.idle_mode = True
        self.idle_mode_interval = 1  # Minimum 1 second as mentioned in the video
        self.idle_mode_variation = 3  # Random variation to make it 1-4 seconds as mentioned in the video
        self.idle_mode_last_time = time.time()
        
        # Eyelid properties
        self.eyelids_closed_height = 0
        self.eyelids_closed_height_next = 0
    
    def update_animations(self, current_time):
        """Update all active animations"""
        # Update auto blinker
        if self.auto_blinker and not self.is_blinking:
            if current_time - self.auto_blinker_last_time > self.auto_blinker_interval + random.uniform(0, self.auto_blinker_variation):
                self.blink()
                self.auto_blinker_last_time = current_time
        
        # Update idle mode
        if self.idle_mode:
            if current_time - self.idle_mode_last_time > self.idle_mode_interval + random.uniform(0, self.idle_mode_variation):
                # Randomly select a new position from the parent's constants
                directions = [self.parent.DEFAULT, self.parent.N, self.parent.NE, 
                              self.parent.E, self.parent.SE, self.parent.S, 
                              self.parent.SW, self.parent.W, self.parent.NW]
                new_position = random.choice(directions)
                self.parent.set_position(new_position)
                self.idle_mode_last_time = current_time
        
        # Update blinking animation
        if self.is_blinking:
            progress = (current_time - self.blink_start_time) / self.blink_duration
            if progress >= 1.0:
                self.is_blinking = False
                self.eyelids_closed_height_next = 0
                self.is_winking = False  # Reset winking state when done
            else:
                # First half closes eyes, second half opens them
                if progress < 0.5:
                    self.eyelids_closed_height_next = int(self.parent.eye_l_height * (progress * 2))
                else:
                    self.eyelids_closed_height_next = int(self.parent.eye_l_height * (1 - (progress - 0.5) * 2))
        
        # Update laughing animation
        if self.is_laughing:
            progress = (current_time - self.laugh_start_time) / self.laugh_duration
            if progress >= 1.0:
                self.is_laughing = False
                self.parent.eye_l_y_next = self.parent.eye_l_y
                self.parent.eye_r_y_next = self.parent.eye_r_y
            else:
                # Oscillate the eyes up and down
                offset = int(math.sin(progress * 10) * 5)
                self.parent.eye_l_y_next = self.parent.eye_l_y + offset
                self.parent.eye_r_y_next = self.parent.eye_r_y + offset
        
        # Update confused animation
        if self.is_confused:
            progress = (current_time - self.confused_start_time) / self.confused_duration
            if progress >= 1.0:
                self.is_confused = False
                self.parent.eye_l_x_next = self.parent.eye_l_x
                self.parent.eye_r_x_next = self.parent.eye_r_x
            else:
                # Oscillate the eyes left and right
                offset = int(math.sin(progress * 10) * 5)
                self.parent.eye_l_x_next = self.parent.eye_l_x + offset
                self.parent.eye_r_x_next = self.parent.eye_r_x + offset
    
    def blink(self):
        """Blink animation with both eyes"""
        if not self.is_blinking:
            self.is_blinking = True
            self.is_winking = False  # Not winking, normal blink
            self.blink_start_time = time.time()
        return True
    
    def wink(self, left_eye=True):
        """Wink animation (blink with only one eye)"""
        if not self.is_blinking:
            self.is_blinking = True
            self.is_winking = True
            self.wink_left_eye = left_eye  # Which eye to wink
            self.blink_start_time = time.time()
        return True
    
    def anim_laugh(self):
        """Laughing animation - eyes shaking up and down"""
        if not self.is_laughing:
            self.is_laughing = True
            self.laugh_start_time = time.time()
        return True
    
    def anim_confused(self):
        """Confused animation - eyes shaking left and right"""
        if not self.is_confused:
            self.is_confused = True
            self.confused_start_time = time.time()
        return True
    
    def set_auto_blinker(self, state, interval=3, variation=2):
        """Set auto blinker state and timing parameters"""
        self.auto_blinker = state
        self.auto_blinker_interval = interval
        self.auto_blinker_variation = variation
        self.auto_blinker_last_time = time.time()
        return True
    
    def set_idle_mode(self, state, interval=1, variation=3):
        """Set idle mode state and timing parameters"""
        self.idle_mode = state
        self.idle_mode_interval = interval
        self.idle_mode_variation = variation
        self.idle_mode_last_time = time.time()
        return True
    
    def draw_eyelids(self, screen, eye_l_x_current, eye_l_y_current, eye_r_x_current, eye_r_y_current, 
                    eye_l_width_current, eye_l_height_current, eye_r_width_current, eye_r_height_current):
        """Draw eyelids based on current animation state"""
        # Smooth transitions for eyelids
        eyelids_closed_height = (self.eyelids_closed_height + self.eyelids_closed_height_next) / 2
        
        # Draw closed eyelids if needed
        if eyelids_closed_height > 0:
            # For winking, only close one eye
            if self.is_winking:
                # Left eye wink
                if self.wink_left_eye:
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),  # BLACK
                        (
                            eye_l_x_current,
                            eye_l_y_current,
                            eye_l_width_current,
                            eyelids_closed_height
                        ),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),  # BLACK
                        (
                            eye_l_x_current,
                            eye_l_y_current + eye_l_height_current - eyelids_closed_height,
                            eye_l_width_current,
                            eyelids_closed_height
                        ),
                        0
                    )
                # Right eye wink
                else:
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),  # BLACK
                        (
                            eye_r_x_current,
                            eye_r_y_current,
                            eye_r_width_current,
                            eyelids_closed_height
                        ),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),  # BLACK
                        (
                            eye_r_x_current,
                            eye_r_y_current + eye_r_height_current - eyelids_closed_height,
                            eye_r_width_current,
                            eyelids_closed_height
                        ),
                        0
                    )
            # Regular blink (both eyes)
            else:
                # Left eye
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_l_x_current,
                        eye_l_y_current,
                        eye_l_width_current,
                        eyelids_closed_height
                    ),
                    0
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_l_x_current,
                        eye_l_y_current + eye_l_height_current - eyelids_closed_height,
                        eye_l_width_current,
                        eyelids_closed_height
                    ),
                    0
                )
                
                # Right eye
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_r_x_current,
                        eye_r_y_current,
                        eye_r_width_current,
                        eyelids_closed_height
                    ),
                    0
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_r_x_current,
                        eye_r_y_current + eye_r_height_current - eyelids_closed_height,
                        eye_r_width_current,
                        eyelids_closed_height
                    ),
                    0
                )
