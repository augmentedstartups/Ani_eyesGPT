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
        # Define valid shapes
        self.valid_shapes = ["round", "square", "pill", "oval", "angry"]

    def set_eye_shape(self, shape):
        """Set the shape of the eyes"""
        if shape in self.valid_shapes:
            self.eye_shape = shape
            # Trigger redraw or update if necessary in parent
            # self.parent.request_update() 
            return True
        print(f"Warning: Invalid eye shape '{shape}'. Valid shapes are: {self.valid_shapes}")
        return False

    def set_width(self, left_eye, right_eye):
        """Set the width of both eyes"""
        # Consider adding validation (e.g., width > 0)
        self.parent.eye_l_width = left_eye
        self.parent.eye_r_width = right_eye
        # Recalculate default positions after size change
        self.set_position(self.parent.current_position if hasattr(self.parent, 'current_position') else DEFAULT)
        return True

    def set_height(self, left_eye, right_eye):
        """Set the height of both eyes"""
        # Consider adding validation (e.g., height > 0)
        self.parent.eye_l_height = left_eye
        self.parent.eye_r_height = right_eye
        # Recalculate default positions after size change
        self.set_position(self.parent.current_position if hasattr(self.parent, 'current_position') else DEFAULT)
        return True

    def set_position(self, position):
        """Set the target eye position (where the eyes should look)"""
        # Ensure parent attributes needed are initialized
        if not all(hasattr(self.parent, attr) for attr in ['screen_width', 'screen_height', 'eye_l_width', 'eye_r_width', 'eye_l_height', 'eye_r_height', 'eye_gap']):
            print("Warning: Parent object missing required attributes for set_position.")
            # Set defaults or return if critical attributes are missing
            # Example: set default values if they don't exist
            self.parent.screen_width = getattr(self.parent, 'screen_width', 800)
            self.parent.screen_height = getattr(self.parent, 'screen_height', 480)
            self.parent.eye_l_width = getattr(self.parent, 'eye_l_width', 100)
            self.parent.eye_r_width = getattr(self.parent, 'eye_r_width', 100)
            self.parent.eye_l_height = getattr(self.parent, 'eye_l_height', 100)
            self.parent.eye_r_height = getattr(self.parent, 'eye_r_height', 100)
            self.parent.eye_gap = getattr(self.parent, 'eye_gap', 50)
            # return False # Optionally stop if setup is incomplete

        center_x = self.parent.screen_width / 2
        center_y = self.parent.screen_height / 2

        # Calculate default position (centered)
        # Ensure these are calculated correctly based on current width/height/gap
        self.parent.eye_l_x_default = center_x - self.parent.eye_l_width - self.parent.eye_gap / 2
        self.parent.eye_r_x_default = center_x + self.parent.eye_gap / 2
        self.parent.eye_l_y_default = center_y - self.parent.eye_l_height / 2
        self.parent.eye_r_y_default = center_y - self.parent.eye_r_height / 2

        # Initialize _next positions to default if they don't exist
        if not hasattr(self.parent, 'eye_l_x_next'): self.parent.eye_l_x_next = self.parent.eye_l_x_default
        if not hasattr(self.parent, 'eye_l_y_next'): self.parent.eye_l_y_next = self.parent.eye_l_y_default
        if not hasattr(self.parent, 'eye_r_x_next'): self.parent.eye_r_x_next = self.parent.eye_r_x_default
        if not hasattr(self.parent, 'eye_r_y_next'): self.parent.eye_r_y_next = self.parent.eye_r_y_default


        # Apply offset based on position - Consider making offset proportional
        # offset_x = self.parent.eye_l_width * 0.1 # Example: 10% of width
        # offset_y = self.parent.eye_l_height * 0.1 # Example: 10% of height
        offset_x = 10 # Keep fixed offset for now
        offset_y = 10 # Keep fixed offset for now
        
        # Calculate target next positions based on direction
        target_l_x = self.parent.eye_l_x_default
        target_l_y = self.parent.eye_l_y_default
        target_r_x = self.parent.eye_r_x_default
        target_r_y = self.parent.eye_r_y_default

        if position == N:
            target_l_y -= offset_y
            target_r_y -= offset_y
        elif position == NE:
            target_l_x += offset_x
            target_l_y -= offset_y
            target_r_x += offset_x
            target_r_y -= offset_y
        elif position == E:
            target_l_x += offset_x
            target_r_x += offset_x
        elif position == SE:
            target_l_x += offset_x
            target_l_y += offset_y
            target_r_x += offset_x
            target_r_y += offset_y
        elif position == S:
            target_l_y += offset_y
            target_r_y += offset_y
        elif position == SW:
            target_l_x -= offset_x
            target_l_y += offset_y
            target_r_x -= offset_x
            target_r_y += offset_y
        elif position == W:
            target_l_x -= offset_x
            target_r_x -= offset_x
        elif position == NW:
            target_l_x -= offset_x
            target_l_y -= offset_y
            target_r_x -= offset_x
            target_r_y -= offset_y
        # Else: DEFAULT, targets remain as default calculated above

        # Set the calculated target positions
        self.parent.eye_l_x_next = target_l_x
        self.parent.eye_l_y_next = target_l_y
        self.parent.eye_r_x_next = target_r_x
        self.parent.eye_r_y_next = target_r_y
        
        # Store the current direction
        self.parent.current_position = position

        return True

    def draw_eyes(self, screen, eye_l_x_current, eye_l_y_current, eye_r_x_current, eye_r_y_current,
                  eye_l_width_current, eye_l_height_current, eye_r_width_current, eye_r_height_current,
                  eye_color):
        """Draw eyes based on selected shape"""
        # Convert all position and size values to integers to avoid float errors
        eye_l_x = int(eye_l_x_current)
        eye_l_y = int(eye_l_y_current)
        eye_r_x = int(eye_r_x_current)
        eye_r_y = int(eye_r_y_current)
        eye_l_width = int(eye_l_width_current)
        eye_l_height = int(eye_l_height_current)
        eye_r_width = int(eye_r_width_current)
        eye_r_height = int(eye_r_height_current)

        if self.eye_shape == "round":
            # Calculate radii for circular eyes (use min dimension for perfect circle)
            radius_l = min(eye_l_width, eye_l_height) // 2
            radius_r = min(eye_r_width, eye_r_height) // 2

            # Calculate circle centers based on the actual bounding box
            center_l_x = eye_l_x + eye_l_width // 2
            center_l_y = eye_l_y + eye_l_height // 2
            center_r_x = eye_r_x + eye_r_width // 2
            center_r_y = eye_r_y + eye_r_height // 2

            # Draw circular eyes
            pygame.draw.circle(screen, eye_color, (center_l_x, center_l_y), radius_l)
            pygame.draw.circle(screen, eye_color, (center_r_x, center_r_y), radius_r)

        elif self.eye_shape == "square":
            # Draw square eyes with rounded corners (radius ~30% of the smaller dimension)
            # Ensure width/height are treated correctly if not equal
            corner_radius_l = min(eye_l_width, eye_l_height) // 3
            corner_radius_r = min(eye_r_width, eye_r_height) // 3

            # Left eye rounded rect
            pygame.draw.rect(screen, eye_color, (eye_l_x, eye_l_y, eye_l_width, eye_l_height), border_radius=corner_radius_l)
            # Right eye rounded rect
            pygame.draw.rect(screen, eye_color, (eye_r_x, eye_r_y, eye_r_width, eye_r_height), border_radius=corner_radius_r)

        elif self.eye_shape == "pill":
            # Draw pill-shaped eyes (capsule shape)
            # Rounded rectangle with radius = half of the height (for horizontal pills)
            # Ensure height > 0 to avoid negative radius
            radius_l = max(1, eye_l_height // 2)
            radius_r = max(1, eye_r_height // 2)
            pygame.draw.rect(screen, eye_color, (eye_l_x, eye_l_y, eye_l_width, eye_l_height), border_radius=radius_l)
            pygame.draw.rect(screen, eye_color, (eye_r_x, eye_r_y, eye_r_width, eye_r_height), border_radius=radius_r)

        elif self.eye_shape == "angry":
            # Draw angry-shaped eyes (angled eyes from image)
            # Ensure parent has a bgcolor attribute for the cut-out
            if not hasattr(self.parent, 'bgcolor'):
                 # Default background if not set in parent - Use black or your actual default
                 print("Warning: Parent object missing 'bgcolor' attribute. Defaulting to black for angry eye cut-out.")
                 self.parent.bgcolor = (0, 0, 0)

            bg_color = self.parent.bgcolor

            # Left eye
            self._draw_angry(
                screen,
                eye_color,
                bg_color, # Pass background color
                eye_l_x,
                eye_l_y,
                eye_l_width,
                eye_l_height,
                is_left_eye=True  # Pass flag for left eye
            )

            # Right eye
            self._draw_angry(
                screen,
                eye_color,
                bg_color, # Pass background color
                eye_r_x,
                eye_r_y,
                eye_r_width,
                eye_r_height,
                is_left_eye=False # Pass flag for right eye
            )

        elif self.eye_shape == "oval":
            # Draw oval-shaped eyes (ellipses) using the bounding box
            # Left eye
            pygame.draw.ellipse(screen, eye_color, (eye_l_x, eye_l_y, eye_l_width, eye_l_height))
            # Right eye
            pygame.draw.ellipse(screen, eye_color, (eye_r_x, eye_r_y, eye_r_width, eye_r_height))

    def _draw_angry(self, screen, color, bg_color, x, y, width, height, is_left_eye):
        # ... (parameter validation, radius calculations as before) ...
        
        # --- NEW: Use a common radius for all corners initially ---
        common_radius = min(width, height) // 3
        common_radius = min(common_radius, width // 2, height // 2)
        common_radius = max(0, common_radius)

        # Angle properties (using user's preferred values)
        angle_height = height // 2 
        angle_width = width // 1 # width
        angle_height = max(0, angle_height)
        angle_width = max(0, angle_width)
        # --- End of Parameters ---

        # 1. Draw the base rectangle with ALL corners rounded (initially)
        try:
            # Pygame >= 2.0.0 needed for border_radius
            pygame.draw.rect(
                screen,
                color,
                (x, y, width, height),
                border_radius=common_radius # Apply radius to ALL corners
            )
        except TypeError:
            # Fallback for older Pygame versions - More complex to do all corners
            print("Warning: Fallback rendering for angry eyes might not show rounded top corners.")
            # Basic rect as fallback placeholder - won't have rounded top corners
            pygame.draw.rect(screen, color, (x, y, width, height)) 
            # Could attempt manual corner drawing here if needed, but gets complex

        # 2. Define points for the triangle to "cut out" the top inner corner
        #    These points remain the same, they define the area to be overlaid with bg_color
        cut_points = []
        if is_left_eye:
            # Left eye: Cut top-right (inner)
            cut_points = [
                (x + width - angle_width, y), # Effectively (x, y) since angle_width = width
                (x + width + 1, y),
                (x + width + 1, y + angle_height)
            ]
        else: # Right eye
            # Right eye: Cut top-left (inner)
            cut_points = [
                (x - 1, y),
                (x + angle_width, y), # Effectively (x + width, y)
                (x - 1, y + angle_height)
            ]

        # 3. Draw the cutting triangle with the background color
        if angle_width > 0 and angle_height > 0 and width > 0 and height > 0:
             pygame.draw.polygon(screen, bg_color, cut_points)