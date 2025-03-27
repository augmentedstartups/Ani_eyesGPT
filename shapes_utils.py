"""
Eye shapes utilities for RoboEyes
Handles all shape-related functionality including different eye shapes,
their rendering, and size/position adjustments.
"""

import pygame
import math

# Direction constants
N = 1   # north, top center
NE = 2  # northeast, top right
E = 3   # east, right center
SE = 4  # southeast, bottom right
S = 5   # south, bottom center
SW = 6  # southwest, bottom left
W = 7   # west, left center
NW = 8  # northwest, top left
DEFAULT = 0  # center

class ShapesHandler:
    def __init__(self, parent):
        """Initialize shapes with reference to parent RoboEyes object"""
        self.parent = parent
        self.eye_shape = "square"  # Default eye shape
        
    def set_eye_shape(self, shape):
        """Set the shape of the eyes"""
        valid_shapes = ["round", "square", "pill", "teardrop", "oval"]
        if shape in valid_shapes:
            self.eye_shape = shape
            return True
        return False
    
    def set_width(self, left_eye, right_eye):
        """Set the width of both eyes"""
        self.parent.eye_l_width = left_eye
        self.parent.eye_r_width = right_eye
        return True
    
    def set_height(self, left_eye, right_eye):
        """Set the height of both eyes"""
        self.parent.eye_l_height = left_eye
        self.parent.eye_r_height = right_eye
        return True

    def set_position(self, position):
        """Set the eye position (where the eyes are looking)"""
        center_x = self.parent.screen_width / 2
        center_y = self.parent.screen_height / 2
        
        # Calculate default position (centered)
        self.parent.eye_l_x_default = center_x - self.parent.eye_l_width - self.parent.eye_gap / 2
        self.parent.eye_r_x_default = center_x + self.parent.eye_gap / 2
        self.parent.eye_l_y_default = center_y - self.parent.eye_l_height / 2
        self.parent.eye_r_y_default = center_y - self.parent.eye_r_height / 2
        
        # Apply offset based on position
        offset_x = 10
        offset_y = 10
        
        if position == N:
            self.parent.eye_l_y_next = self.parent.eye_l_y_default - offset_y
            self.parent.eye_r_y_next = self.parent.eye_r_y_default - offset_y
        elif position == NE:
            self.parent.eye_l_x_next = self.parent.eye_l_x_default + offset_x
            self.parent.eye_l_y_next = self.parent.eye_l_y_default - offset_y
            self.parent.eye_r_x_next = self.parent.eye_r_x_default + offset_x
            self.parent.eye_r_y_next = self.parent.eye_r_y_default - offset_y
        elif position == E:
            self.parent.eye_l_x_next = self.parent.eye_l_x_default + offset_x
            self.parent.eye_r_x_next = self.parent.eye_r_x_default + offset_x
        elif position == SE:
            self.parent.eye_l_x_next = self.parent.eye_l_x_default + offset_x
            self.parent.eye_l_y_next = self.parent.eye_l_y_default + offset_y
            self.parent.eye_r_x_next = self.parent.eye_r_x_default + offset_x
            self.parent.eye_r_y_next = self.parent.eye_r_y_default + offset_y
        elif position == S:
            self.parent.eye_l_y_next = self.parent.eye_l_y_default + offset_y
            self.parent.eye_r_y_next = self.parent.eye_r_y_default + offset_y
        elif position == SW:
            self.parent.eye_l_x_next = self.parent.eye_l_x_default - offset_x
            self.parent.eye_l_y_next = self.parent.eye_l_y_default + offset_y
            self.parent.eye_r_x_next = self.parent.eye_r_x_default - offset_x
            self.parent.eye_r_y_next = self.parent.eye_r_y_default + offset_y
        elif position == W:
            self.parent.eye_l_x_next = self.parent.eye_l_x_default - offset_x
            self.parent.eye_r_x_next = self.parent.eye_r_x_default - offset_x
        elif position == NW:
            self.parent.eye_l_x_next = self.parent.eye_l_x_default - offset_x
            self.parent.eye_l_y_next = self.parent.eye_l_y_default - offset_y
            self.parent.eye_r_x_next = self.parent.eye_r_x_default - offset_x
            self.parent.eye_r_y_next = self.parent.eye_r_y_default - offset_y
        else:  # DEFAULT
            self.parent.eye_l_x_next = self.parent.eye_l_x_default
            self.parent.eye_l_y_next = self.parent.eye_l_y_default
            self.parent.eye_r_x_next = self.parent.eye_r_x_default
            self.parent.eye_r_y_next = self.parent.eye_r_y_default
        
        return True
    
    def draw_eyes(self, screen, eye_l_x_current, eye_l_y_current, eye_r_x_current, eye_r_y_current, 
                  eye_l_width_current, eye_l_height_current, eye_r_width_current, eye_r_height_current, 
                  eye_color):
        """Draw eyes based on selected shape"""
        if self.eye_shape == "round":
            # Calculate radii for circular eyes
            radius_l = min(eye_l_width_current, eye_l_height_current) // 2
            radius_r = min(eye_r_width_current, eye_r_height_current) // 2
            
            # Calculate circle centers
            center_l_x = eye_l_x_current + eye_l_width_current // 2
            center_l_y = eye_l_y_current + eye_l_height_current // 2
            center_r_x = eye_r_x_current + eye_r_width_current // 2
            center_r_y = eye_r_y_current + eye_r_height_current // 2
            
            # Draw circular eyes
            pygame.draw.circle(screen, eye_color, (center_l_x, center_l_y), radius_l)
            pygame.draw.circle(screen, eye_color, (center_r_x, center_r_y), radius_r)
            
        elif self.eye_shape == "square":
            # Draw square eyes with rounded corners (radius is 30% of the smaller dimension)
            corner_radius_l = min(eye_l_width_current, eye_l_height_current) // 3
            corner_radius_r = min(eye_r_width_current, eye_r_height_current) // 3
            
            # Left eye rounded rect
            pygame.draw.rect(
                screen, 
                eye_color, 
                (
                    eye_l_x_current, 
                    eye_l_y_current, 
                    eye_l_width_current, 
                    eye_l_height_current
                ), 
                0, 
                corner_radius_l
            )
            
            # Right eye rounded rect
            pygame.draw.rect(
                screen, 
                eye_color, 
                (
                    eye_r_x_current, 
                    eye_r_y_current, 
                    eye_r_width_current, 
                    eye_r_height_current
                ), 
                0, 
                corner_radius_r
            )
            
        elif self.eye_shape == "pill":
            # Draw pill-shaped eyes (capsule shape)
            # Draw rounded rectangle with radius = half of height
            pygame.draw.rect(
                screen, 
                eye_color, 
                (
                    eye_l_x_current, 
                    eye_l_y_current, 
                    eye_l_width_current, 
                    eye_l_height_current
                ), 
                0, 
                eye_l_height_current // 2
            )
            
            pygame.draw.rect(
                screen, 
                eye_color, 
                (
                    eye_r_x_current, 
                    eye_r_y_current, 
                    eye_r_width_current, 
                    eye_r_height_current
                ), 
                0, 
                eye_r_height_current // 2
            )
            
        elif self.eye_shape == "teardrop":
            # Draw teardrop-shaped eyes
            # This is a custom shape for the SAD mood
            # Left eye
            self._draw_teardrop(
                screen, 
                eye_color,
                eye_l_x_current + eye_l_width_current // 2,  # center x
                eye_l_y_current + eye_l_height_current // 2,  # center y
                eye_l_width_current // 2,  # radius x
                eye_l_height_current // 2   # radius y
            )
            
            # Right eye
            self._draw_teardrop(
                screen, 
                eye_color,
                eye_r_x_current + eye_r_width_current // 2,  # center x
                eye_r_y_current + eye_r_height_current // 2,  # center y
                eye_r_width_current // 2,  # radius x
                eye_r_height_current // 2   # radius y
            )
            
        elif self.eye_shape == "oval":
            # Draw oval-shaped eyes (ellipses)
            # Left eye
            pygame.draw.ellipse(
                screen, 
                eye_color, 
                (
                    eye_l_x_current, 
                    eye_l_y_current, 
                    eye_l_width_current, 
                    eye_l_height_current
                )
            )
            
            # Right eye
            pygame.draw.ellipse(
                screen, 
                eye_color, 
                (
                    eye_r_x_current, 
                    eye_r_y_current, 
                    eye_r_width_current, 
                    eye_r_height_current
                )
            )
    
    def _draw_teardrop(self, screen, color, center_x, center_y, radius_x, radius_y):
        """Helper method to draw a teardrop shape"""
        # A teardrop is like an oval with a pointed bottom
        # First draw the oval part
        pygame.draw.ellipse(
            screen,
            color,
            (
                center_x - radius_x,
                center_y - radius_y,
                radius_x * 2,
                radius_y * 2
            )
        )
        
        # Then draw a triangle to create the pointed bottom
        points = [
            (center_x - radius_x // 2, center_y + radius_y // 2),  # Left point
            (center_x + radius_x // 2, center_y + radius_y // 2),  # Right point
            (center_x, center_y + radius_y * 2)                    # Bottom point
        ]
        pygame.draw.polygon(screen, color, points)
