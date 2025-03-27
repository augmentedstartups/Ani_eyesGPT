"""
RoboEyes Python Implementation
Based on the FluxGarage RoboEyes library for Arduino
Draws smoothly animated robot eyes on a window using Pygame

Original library by Dennis Hoelscher (FluxGarage)
Python implementation created as a standalone version
"""

import pygame
import random
import time
import math

# Import utility modules
from utils.animations_utils import AnimationsHandler
from utils.moods_utils import MoodsHandler, DEFAULT, TIRED, SAD, EXCITED
from utils.shapes_utils import ShapesHandler, N, NE, E, SE, S, SW, W, NW

# Colors
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)  # Using cyan color for the eyes as shown in the images
WHITE = (255, 255, 255)

class RoboEyes:
    def __init__(self):
        # Screen properties
        self.screen_width = 640  # Default window width
        self.screen_height = 320  # Default window height
        self.max_fps = 60  # Default max frame rate
        self.screen = None
        self.clock = None
        self.running = False
        
        # Force default mood on startup
        self.startup_complete = False
        
        # Initialize utility handlers (will be properly initialized in begin())
        self.animations = None
        self.moods = None
        self.shapes = None

        # Eye properties
        self.eye_l_width = 36
        self.eye_l_height = 36
        self.eye_l_border_radius = 8
        self.eye_r_width = 36
        self.eye_r_height = 36
        self.eye_r_border_radius = 8
        self.space_between = 10

        # Current and target values for smooth transitions
        self.eye_l_width_current = self.eye_l_width
        self.eye_l_height_current = self.eye_l_height
        self.eye_l_border_radius_current = self.eye_l_border_radius
        self.eye_r_width_current = self.eye_r_width
        self.eye_r_height_current = self.eye_r_height
        self.eye_r_border_radius_current = self.eye_r_border_radius

        # Default values (used for resetting)
        self.eye_l_width_default = self.eye_l_width
        self.eye_l_height_default = self.eye_l_height
        self.eye_l_border_radius_default = self.eye_l_border_radius
        self.eye_r_width_default = self.eye_r_width
        self.eye_r_height_default = self.eye_r_height
        self.eye_r_border_radius_default = self.eye_r_border_radius

        # Eye positions
        self.eye_l_x = 0
        self.eye_l_y = 0
        self.eye_r_x = 0
        self.eye_r_y = 0

        # Target positions for smooth transitions
        self.eye_l_x_next = 0
        self.eye_l_y_next = 0
        self.eye_r_x_next = 0
        self.eye_r_y_next = 0

        # Eyelid properties
        self.eyelids_closed_height = 0
        self.eyelids_closed_height_next = 0
        self.eyelids_tired_height = 0
        self.eyelids_tired_height_next = 0
        self.eyelids_angry_height = 0
        self.eyelids_angry_height_next = 0
        self.eyelids_happy_bottom_offset = 0
        self.eyelids_happy_bottom_offset_next = 0

        # Animation properties
        self.mood = DEFAULT
        self.cyclops = False
        self.curiosity = False
        self.h_flicker = False
        self.h_flicker_amplitude = 0
        self.v_flicker = False
        self.v_flicker_amplitude = 0
        self.auto_blinker = False
        self.auto_blinker_interval = 3
        self.auto_blinker_variation = 2
        self.auto_blinker_last_time = 0
        self.idle_mode = False
        self.idle_mode_interval = 2
        self.idle_mode_variation = 2
        self.idle_mode_last_time = 0
        self.position = DEFAULT

        # Animation state
        self.is_blinking = False
        self.is_winking = False
        self.blink_start_time = 0
        self.blink_duration = 0.3  # seconds
        self.is_laughing = False
        self.laugh_start_time = 0
        self.laugh_duration = 1.0  # seconds
        self.is_confused = False
        self.confused_start_time = 0
        self.confused_duration = 1.0  # seconds
        
        # Eye shape variations
        self.eye_shape = "square"  # Can be "round", "square", "oval", "teardrop", "pill"
        
        # Manual eye control with arrow keys (enabled by default)
        self.manual_control = True
        self.manual_x_offset = 0
        self.manual_y_offset = 0
        self.manual_x_velocity = 0
        self.manual_y_velocity = 0
        self.manual_velocity_max = 5  # Maximum velocity for arrow key movement
        self.manual_velocity_accel = 0.5  # Acceleration factor
        self.manual_velocity_decel = 0.9  # Deceleration factor (friction)
        self.manual_offset_max = 50  # Maximum pixel offset for manual control
        self.last_key_press_time = time.time()
        self.auto_center_delay = 5.0  # Seconds of inactivity before auto-centering
        
        # Initialize eyelid properties
        self.eyelids_closed_height = 0
        self.eyelids_closed_height_next = 0
        self.eyelids_tired_height = 0
        self.eyelids_tired_height_next = 0
        
        # Auto animations
        self.auto_blinker = True
        self.auto_blinker_interval = 3
        self.auto_blinker_variation = 2
        self.auto_blinker_last_time = time.time()
        self.idle_mode = True
        self.idle_mode_interval = 4
        self.idle_mode_variation = 2
        self.idle_mode_last_time = time.time()

    def begin(self, screen_width, screen_height, max_fps=60):
        """Initialize the RoboEyes with screen dimensions and frame rate"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_fps = max_fps
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("RoboEyes Python")
        self.clock = pygame.time.Clock()
        
        # Initialize utility handlers
        self.animations = AnimationsHandler(self)
        self.moods = MoodsHandler(self)
        self.shapes = ShapesHandler(self)
        
        # Calculate initial eye positions
        self._calculate_eye_positions()
        
        # Ensure we start with the correct eye shape
        self.shapes.set_eye_shape("square")
        
        # Add some size variability between eyes
        self.eye_r_width = int(self.eye_r_width * 0.95)  # Right eye slightly narrower
        self.eye_r_height = int(self.eye_r_height * 1.05)  # Right eye slightly taller
        
        # Force default mood on startup
        self.moods.set_mood(DEFAULT)
        
        self.running = True
        self.startup_complete = True
        return True

    def _calculate_eye_positions(self):
        """Calculate the eye positions based on screen size and eye properties"""
        # Calculate positions for both eyes (cyclops mode disabled)
        total_width = self.eye_l_width + self.eye_r_width + self.space_between
        self.eye_l_x = (self.screen_width - total_width) // 2
        self.eye_l_y = (self.screen_height - self.eye_l_height) // 2
        self.eye_r_x = self.eye_l_x + self.eye_l_width + self.space_between
        self.eye_r_y = (self.screen_height - self.eye_r_height) // 2
        
        self.eye_l_x_next = self.eye_l_x
        self.eye_l_y_next = self.eye_l_y
        self.eye_r_x_next = self.eye_r_x
        self.eye_r_y_next = self.eye_r_y

    def update(self):
        """Update eyes drawings with frame rate limitation"""
        if not self.running:
            return False
            
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                return False
                
        # Force default mood on first frame
        if not self.startup_complete:
            self.set_mood(DEFAULT)
            self.startup_complete = True
        
        # Handle arrow key input for manual eye control with velocity
        keys = pygame.key.get_pressed()
        key_pressed = keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        
        if key_pressed:
            # Update last key press time when any arrow key is pressed
            self.last_key_press_time = time.time()
        
        # Check if we should auto-center due to inactivity
        current_time = time.time()
        if current_time - self.last_key_press_time > self.auto_center_delay:
            # Gradually move back to center
            self.manual_x_offset *= 0.95
            self.manual_y_offset *= 0.95
            self.manual_x_velocity = 0
            self.manual_y_velocity = 0
            # Consider centered when very close to center
            if abs(self.manual_x_offset) < 0.5 and abs(self.manual_y_offset) < 0.5:
                self.manual_x_offset = 0
                self.manual_y_offset = 0
        
        # Apply acceleration based on arrow keys
        if keys[pygame.K_UP]:
            self.manual_y_velocity -= self.manual_velocity_accel
        if keys[pygame.K_DOWN]:
            self.manual_y_velocity += self.manual_velocity_accel
        if keys[pygame.K_LEFT]:
            self.manual_x_velocity -= self.manual_velocity_accel
        if keys[pygame.K_RIGHT]:
            self.manual_x_velocity += self.manual_velocity_accel
            
        # Apply velocity limits
        self.manual_x_velocity = max(-self.manual_velocity_max, min(self.manual_velocity_max, self.manual_x_velocity))
        self.manual_y_velocity = max(-self.manual_velocity_max, min(self.manual_velocity_max, self.manual_y_velocity))
        
        # Apply deceleration (friction) when no keys are pressed
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.manual_x_velocity *= self.manual_velocity_decel
        if not (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.manual_y_velocity *= self.manual_velocity_decel
            
        # Apply velocity to position
        self.manual_x_offset += self.manual_x_velocity
        self.manual_y_offset += self.manual_y_velocity
        
        # Apply position limits
        self.manual_x_offset = max(-self.manual_offset_max, min(self.manual_offset_max, self.manual_x_offset))
        self.manual_y_offset = max(-self.manual_offset_max, min(self.manual_offset_max, self.manual_y_offset))
        
        # Stop completely if velocity is very small
        if abs(self.manual_x_velocity) < 0.1:
            self.manual_x_velocity = 0
        if abs(self.manual_y_velocity) < 0.1:
            self.manual_y_velocity = 0
        
        # Clear the screen
        self.screen.fill(BLACK)
        
        # Update animations
        self._update_animations()
        
        # Draw the eyes
        self._draw_eyes()
        
        # Update display
        pygame.display.flip()
        
        # Limit frame rate
        self.clock.tick(self.max_fps)
        
        return True

    def _update_animations(self):
        """Update all active animations"""
        current_time = time.time()
        
        # Use the animations handler to update all animations
        self.animations.update_animations(current_time)
        
        # Update flicker (keeping this in main class for now)
        if self.h_flicker:
            offset = random.randint(-self.h_flicker_amplitude, self.h_flicker_amplitude)
            self.eye_l_x_next = self.eye_l_x + offset
            self.eye_r_x_next = self.eye_r_x + offset
        
        if self.v_flicker:
            offset = random.randint(-self.v_flicker_amplitude, self.v_flicker_amplitude)
            self.eye_l_y_next = self.eye_l_y + offset
            self.eye_r_y_next = self.eye_r_y + offset

    def _draw_eyes(self):
        """Draw the eyes with current properties"""
        # Smooth transitions for all properties
        self.eye_l_width_current = (self.eye_l_width_current + self.eye_l_width) / 2
        self.eye_l_height_current = (self.eye_l_height_current + self.eye_l_height) / 2
        self.eye_l_border_radius_current = (self.eye_l_border_radius_current + self.eye_l_border_radius) / 2
        self.eye_r_width_current = (self.eye_r_width_current + self.eye_r_width) / 2
        self.eye_r_height_current = (self.eye_r_height_current + self.eye_r_height) / 2
        self.eye_r_border_radius_current = (self.eye_r_border_radius_current + self.eye_r_border_radius) / 2
        
        # Smooth transitions for positions
        eye_l_x_current = (self.eye_l_x + self.eye_l_x_next) / 2
        eye_l_y_current = (self.eye_l_y + self.eye_l_y_next) / 2
        eye_r_x_current = (self.eye_r_x + self.eye_r_x_next) / 2
        eye_r_y_current = (self.eye_r_y + self.eye_r_y_next) / 2
        
        # Apply manual control offsets if enabled
        if self.manual_control:
            eye_l_x_current += self.manual_x_offset
            eye_l_y_current += self.manual_y_offset
            eye_r_x_current += self.manual_x_offset
            eye_r_y_current += self.manual_y_offset
        
        # Use the shapes handler to draw the eyes
        self.shapes.draw_eyes(
            self.screen,
            eye_l_x_current, eye_l_y_current,
            eye_r_x_current, eye_r_y_current,
            self.eye_l_width_current, self.eye_l_height_current,
            self.eye_r_width_current, self.eye_r_height_current,
            CYAN
        )
        
        # Use the animations handler to draw eyelids for blinking/winking
        self.animations.draw_eyelids(
            self.screen,
            eye_l_x_current, eye_l_y_current,
            eye_r_x_current, eye_r_y_current,
            self.eye_l_width_current, self.eye_l_height_current,
            self.eye_r_width_current, self.eye_r_height_current
        )
        
        # Use the moods handler to draw mood-specific elements
        self.moods.draw_mood_elements(
            self.screen,
            eye_l_x_current, eye_l_y_current,
            eye_r_x_current, eye_r_y_current,
            self.eye_l_width_current, self.eye_l_height_current,
            self.eye_r_width_current, self.eye_r_height_current
        )
        
        # Draw tired eyelids if in TIRED mood
        if self.mood == TIRED and eyelids_tired_height > 0:
            # Left eye (or single eye in cyclops mode)
            pygame.draw.rect(
                self.screen,
                BLACK,
                (
                    eye_l_x_current,
                    eye_l_y_current,
                    self.eye_l_width_current,
                    eyelids_tired_height
                ),
                0
            )
            
            # Right eye (if not in cyclops mode)
            if not self.cyclops:
                pygame.draw.rect(
                    self.screen,
                    BLACK,
                    (
                        eye_r_x_current,
                        eye_r_y_current,
                        self.eye_r_width_current,
                        eyelids_tired_height
                    ),
                    0
                )
        


    # Eye shape configuration methods
    def set_width(self, left_eye, right_eye):
        """Set the width of both eyes"""
        self.eye_l_width = left_eye
        self.eye_r_width = right_eye
        self._calculate_eye_positions()
        return True

    def set_height(self, left_eye, right_eye):
        """Set the height of both eyes"""
        self.eye_l_height = left_eye
        self.eye_r_height = right_eye
        self._calculate_eye_positions()
        return True

    def set_border_radius(self, left_eye, right_eye):
        """Set the border radius of both eyes"""
        self.eye_l_border_radius = left_eye
        self.eye_r_border_radius = right_eye
        return True

    def set_space_between(self, space):
        """Set the space between eyes"""
        self.space_between = space
        self._calculate_eye_positions()
        return True

    def set_cyclops(self, state):
        """Set cyclops mode (single eye) - DISABLED"""
        # Always set to False to disable cyclops mode
        self.cyclops = False
        self._calculate_eye_positions()
        return True

    # Mood and expression methods
    def set_mood(self, mood):
        """Set the mood expression"""
        return self.moods.set_mood(mood)
        
        return True

    def set_position(self, position):
        """Set the eye position using cardinal directions"""
        self.position = position
        
        # Calculate base positions
        base_l_x = (self.screen_width - (self.eye_l_width + self.eye_r_width + self.space_between)) // 2
        base_l_y = (self.screen_height - self.eye_l_height) // 2
        base_r_x = base_l_x + self.eye_l_width + self.space_between
        base_r_y = (self.screen_height - self.eye_r_height) // 2
        
        # Offset for eye movement (about 10% of eye size)
        offset_x = int(self.eye_l_width * 0.1)
        offset_y = int(self.eye_l_height * 0.1)
        
        # Set positions based on direction
        if position == DEFAULT:
            self.eye_l_x_next = base_l_x
            self.eye_l_y_next = base_l_y
            self.eye_r_x_next = base_r_x
            self.eye_r_y_next = base_r_y
        elif position == N:  # North (top)
            self.eye_l_x_next = base_l_x
            self.eye_l_y_next = base_l_y - offset_y
            self.eye_r_x_next = base_r_x
            self.eye_r_y_next = base_r_y - offset_y
        elif position == NE:  # Northeast (top right)
            self.eye_l_x_next = base_l_x + offset_x
            self.eye_l_y_next = base_l_y - offset_y
            self.eye_r_x_next = base_r_x + offset_x
            self.eye_r_y_next = base_r_y - offset_y
        elif position == E:  # East (right)
            self.eye_l_x_next = base_l_x + offset_x
            self.eye_l_y_next = base_l_y
            self.eye_r_x_next = base_r_x + offset_x
            self.eye_r_y_next = base_r_y
        elif position == SE:  # Southeast (bottom right)
            self.eye_l_x_next = base_l_x + offset_x
            self.eye_l_y_next = base_l_y + offset_y
            self.eye_r_x_next = base_r_x + offset_x
            self.eye_r_y_next = base_r_y + offset_y
        elif position == S:  # South (bottom)
            self.eye_l_x_next = base_l_x
            self.eye_l_y_next = base_l_y + offset_y
            self.eye_r_x_next = base_r_x
            self.eye_r_y_next = base_r_y + offset_y
        elif position == SW:  # Southwest (bottom left)
            self.eye_l_x_next = base_l_x - offset_x
            self.eye_l_y_next = base_l_y + offset_y
            self.eye_r_x_next = base_r_x - offset_x
            self.eye_r_y_next = base_r_y + offset_y
        elif position == W:  # West (left)
            self.eye_l_x_next = base_l_x - offset_x
            self.eye_l_y_next = base_l_y
            self.eye_r_x_next = base_r_x - offset_x
            self.eye_r_y_next = base_r_y
        elif position == NW:  # Northwest (top left)
            self.eye_l_x_next = base_l_x - offset_x
            self.eye_l_y_next = base_l_y - offset_y
            self.eye_r_x_next = base_r_x - offset_x
            self.eye_r_y_next = base_r_y - offset_y
        
        # Apply curiosity effect if enabled
        if self.curiosity and (position == E or position == W):
            if position == E:
                self.eye_r_height = int(self.eye_r_height_default * 1.2)
            elif position == W:
                self.eye_l_height = int(self.eye_l_height_default * 1.2)
        else:
            self.eye_l_height = self.eye_l_height_default
            self.eye_r_height = self.eye_r_height_default
        
        return True

    def set_curiosity(self, state):
        """Enable/disable curiosity effect"""
        self.curiosity = state
        return True

    def open(self, left_eye=True, right_eye=True):
        """Open eyes"""
        if left_eye:
            self.eyelids_closed_height_next = 0
        if right_eye and not self.cyclops:
            self.eyelids_closed_height_next = 0
        return True

    def close(self, left_eye=True, right_eye=True):
        """Close eyes"""
        if left_eye:
            self.eyelids_closed_height_next = self.eye_l_height
        if right_eye and not self.cyclops:
            self.eyelids_closed_height_next = self.eye_r_height
        return True

    # Flicker methods
    def set_h_flicker(self, state, amplitude=2):
        """Set horizontal flicker"""
        self.h_flicker = state
        self.h_flicker_amplitude = amplitude
        return True

    def set_v_flicker(self, state, amplitude=2):
        """Set vertical flicker"""
        self.v_flicker = state
        self.v_flicker_amplitude = amplitude
        return True

    # Animation methods
    def blink(self, left_eye=True, right_eye=True):
        """Blink animation"""
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
        """Laughing animation"""
        if not self.is_laughing:
            self.is_laughing = True
            self.laugh_start_time = time.time()
        return True

    def anim_confused(self):
        """Confused animation"""
        if not self.is_confused:
            self.is_confused = True
            self.confused_start_time = time.time()
        return True

    # Macro animators
    def set_auto_blinker(self, state, interval=3, variation=2):
        """Set auto blinker"""
        self.auto_blinker = state
        self.auto_blinker_interval = interval
        self.auto_blinker_variation = variation
        self.auto_blinker_last_time = time.time()
        return True

    def set_idle_mode(self, state, interval=2, variation=2):
        """Set idle mode"""
        self.idle_mode = state
        self.idle_mode_interval = interval
        self.idle_mode_variation = variation
        self.idle_mode_last_time = time.time()
        return True
        
    def set_eye_shape(self, shape):
        """Set the eye shape"""
        if shape in ["round", "square", "oval", "teardrop", "pill"]:
            self.eye_shape = shape
            return True
        return False
        
    def set_manual_control(self, state):
        """Enable/disable manual control with arrow keys"""
        self.manual_control = state
        # Reset offsets and velocities when disabling manual control
        if not state:
            self.manual_x_offset = 0
            self.manual_y_offset = 0
            self.manual_x_velocity = 0
            self.manual_y_velocity = 0
        return True
        
    def anim_excited(self):
        """Excited animation - rapidly changing eye size"""
        self.set_mood(EXCITED)
        self.set_h_flicker(True, 3)
        self.set_v_flicker(True, 3)
        return True

    def is_running(self):
        """Check if the animation is still running"""
        return self.running

    def quit(self):
        """Quit pygame and clean up"""
        self.running = False
        pygame.quit()
