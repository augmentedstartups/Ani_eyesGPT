"""
Moods utilities for RoboEyes
Handles all mood-related functionality including different eye expressions 
and appearance changes based on mood.
"""

import pygame

# Define mood constants
DEFAULT = 0
TIRED = 1
SAD = 2
EXCITED = 3

class MoodsHandler:
    def __init__(self, parent):
        """Initialize moods with reference to parent RoboEyes object"""
        self.parent = parent
        self.current_mood = DEFAULT
        
        # Eyelid properties for mood expressions
        self.eyelids_tired_height = 0
        self.eyelids_tired_height_next = 0
    
    def set_mood(self, mood):
        """Set the mood expression"""
        self.current_mood = mood
        
        # Reset all mood-related properties
        self.eyelids_tired_height_next = 0
        
        # Set the appropriate mood properties and eye shapes
        if mood == TIRED:
            self.eyelids_tired_height_next = int(self.parent.eye_l_height * 0.3)
            self.parent.shapes.set_eye_shape("square")
        elif mood == SAD:
            # Angry shape for SAD mood as shown in the image
            self.parent.shapes.set_eye_shape("angry")
            # Make eyes slightly narrower
            self.parent.shapes.set_width(
                int(self.parent.eye_l_width_default * 0.9), 
                int(self.parent.eye_r_width_default * 0.9)
            )
            self.parent.shapes.set_height(
                self.parent.eye_l_height_default, 
                self.parent.eye_r_height_default
            )
        elif mood == EXCITED:
            self.parent.shapes.set_eye_shape("pill")
            # Make eyes wider for excited look
            self.parent.shapes.set_width(
                int(self.parent.eye_l_width_default * 1.3), 
                int(self.parent.eye_r_width_default * 1.3)
            )
            self.parent.shapes.set_height(
                int(self.parent.eye_l_height_default * 0.8), 
                int(self.parent.eye_r_height_default * 0.8)
            )
            # Add asymmetry for more character
            self.parent.eye_r_width = int(self.parent.eye_r_width * 0.9)  # Right eye slightly narrower
        else:  # DEFAULT
            # Reset to default eye shape and size with slight asymmetry
            self.parent.shapes.set_eye_shape("square")
            self.parent.shapes.set_width(
                self.parent.eye_l_width_default, 
                int(self.parent.eye_r_width_default * 0.95)
            )
            self.parent.shapes.set_height(
                self.parent.eye_l_height_default, 
                int(self.parent.eye_r_height_default * 1.05)
            )
        
        return True

    def get_current_mood(self):
        """Get the current mood value"""
        return self.current_mood
    
    def draw_mood_elements(self, screen, eye_l_x_current, eye_l_y_current, eye_r_x_current, eye_r_y_current, 
                          eye_l_width_current, eye_l_height_current, eye_r_width_current, eye_r_height_current):
        """Draw mood-specific elements"""
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
        eyelids_tired_height = int((self.eyelids_tired_height + self.eyelids_tired_height_next) / 2)
        
        # Draw tired eyelids if in TIRED mood
        if self.current_mood == TIRED and eyelids_tired_height > 0:
            # Left eye
            pygame.draw.rect(
                screen,
                (0, 0, 0),  # BLACK
                (
                    eye_l_x,
                    eye_l_y,
                    eye_l_width,
                    eyelids_tired_height
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
                    eyelids_tired_height
                ),
                0
            )
