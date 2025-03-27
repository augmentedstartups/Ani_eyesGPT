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
        
        # Idle mode with smooth movement
        self.idle_mode = True
        self.idle_mode_interval = 1  # Minimum 1 second as mentioned in the video
        self.idle_mode_variation = 3  # Random variation to make it 1-4 seconds as mentioned in the video
        self.idle_mode_last_time = time.time()
        self.idle_target_position = 0  # Target position to move to
        self.idle_current_position = 0  # Current position
        self.idle_velocity_x = 0  # X velocity for smooth movement
        self.idle_velocity_y = 0  # Y velocity for smooth movement
        self.idle_acceleration = 0.2  # Acceleration factor
        self.idle_deceleration = 0.9  # Deceleration factor (friction)
        self.idle_max_velocity = 3  # Maximum velocity
        self.idle_moving = False  # Whether currently moving to a target
        
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
        
        # Update idle mode with smooth movement
        if self.idle_mode:
            # Import the constants directly from shapes_utils
            from utils.shapes_utils import DEFAULT, N, NE, E, SE, S, SW, W, NW
            
            # Check if it's time to select a new target position
            if not self.idle_moving or (current_time - self.idle_mode_last_time > self.idle_mode_interval + random.uniform(0, self.idle_mode_variation)):
                # Randomly select a new position
                directions = [DEFAULT, N, NE, E, SE, S, SW, W, NW]
                self.idle_target_position = random.choice(directions)
                self.idle_moving = True
                self.idle_mode_last_time = current_time
                
                # Set target coordinates based on the selected position
                if self.idle_target_position == N:
                    target_x = 0
                    target_y = -1
                elif self.idle_target_position == NE:
                    target_x = 1
                    target_y = -1
                elif self.idle_target_position == E:
                    target_x = 1
                    target_y = 0
                elif self.idle_target_position == SE:
                    target_x = 1
                    target_y = 1
                elif self.idle_target_position == S:
                    target_x = 0
                    target_y = 1
                elif self.idle_target_position == SW:
                    target_x = -1
                    target_y = 1
                elif self.idle_target_position == W:
                    target_x = -1
                    target_y = 0
                elif self.idle_target_position == NW:
                    target_x = -1
                    target_y = -1
                else:  # DEFAULT
                    target_x = 0
                    target_y = 0
                
                # Apply acceleration toward target
                self.idle_velocity_x += target_x * self.idle_acceleration
                self.idle_velocity_y += target_y * self.idle_acceleration
                
                # Apply velocity limits
                self.idle_velocity_x = max(-self.idle_max_velocity, min(self.idle_max_velocity, self.idle_velocity_x))
                self.idle_velocity_y = max(-self.idle_max_velocity, min(self.idle_max_velocity, self.idle_velocity_y))
            
            # Apply deceleration when close to target
            if self.idle_moving and self.idle_target_position == DEFAULT:
                self.idle_velocity_x *= self.idle_deceleration
                self.idle_velocity_y *= self.idle_deceleration
                
                # Stop when velocity is very small
                if abs(self.idle_velocity_x) < 0.1 and abs(self.idle_velocity_y) < 0.1:
                    self.idle_velocity_x = 0
                    self.idle_velocity_y = 0
                    self.idle_moving = False
            
            # Apply the velocity to the eye position
            base_offset = 10  # Base offset for eye movement
            self.parent.eye_l_x_next = self.parent.eye_l_x + int(self.idle_velocity_x * base_offset)
            self.parent.eye_l_y_next = self.parent.eye_l_y + int(self.idle_velocity_y * base_offset)
            self.parent.eye_r_x_next = self.parent.eye_r_x + int(self.idle_velocity_x * base_offset)
            self.parent.eye_r_y_next = self.parent.eye_r_y + int(self.idle_velocity_y * base_offset)
        
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
        # Convert all position and size values to integers to avoid float errors
        eye_l_x = int(eye_l_x_current)
        eye_l_y = int(eye_l_y_current)
        eye_r_x = int(eye_r_x_current)
        eye_r_y = int(eye_r_y_current)
        eye_l_width = int(eye_l_width_current)
        eye_l_height = int(eye_l_height_current)
        eye_r_width = int(eye_r_width_current)
        eye_r_height = int(eye_r_height_current)
        
        # Smooth transitions for eyelids
        eyelids_closed_height = int((self.eyelids_closed_height + self.eyelids_closed_height_next) / 2)
        
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
                            eye_l_x,
                            eye_l_y,
                            eye_l_width,
                            eyelids_closed_height
                        ),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),  # BLACK
                        (
                            eye_l_x,
                            eye_l_y + eye_l_height - eyelids_closed_height,
                            eye_l_width,
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
                            eye_r_x,
                            eye_r_y,
                            eye_r_width,
                            eyelids_closed_height
                        ),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),  # BLACK
                        (
                            eye_r_x,
                            eye_r_y + eye_r_height - eyelids_closed_height,
                            eye_r_width,
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
                        eye_l_x,
                        eye_l_y,
                        eye_l_width,
                        eyelids_closed_height
                    ),
                    0
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_l_x,
                        eye_l_y + eye_l_height - eyelids_closed_height,
                        eye_l_width,
                        eyelids_closed_height
                    ),
                    0
                )
                
                # Right eye
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_r_x,
                        eye_r_y,
                        eye_r_width,
                        eyelids_closed_height
                    ),
                    0
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # BLACK
                    (
                        eye_r_x,
                        eye_r_y + eye_r_height - eyelids_closed_height,
                        eye_r_width,
                        eyelids_closed_height
                    ),
                    0
                )
