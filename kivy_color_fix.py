"""
Color scheme fix for VirtualDoctor Kivy applications
This script applies consistent color improvements for better text visibility
"""

# Color definitions for better visibility
COLORS = {
    'background_dark': (0.1, 0.1, 0.3, 1),      # Dark blue background
    'background_light': (0.95, 0.95, 0.95, 1),   # Light gray background
    'text_on_dark': (1, 1, 1, 1),                # White text on dark background
    'text_on_light': (0, 0, 0, 1),               # Black text on light background
    'button_primary': (0.2, 0.6, 0.8, 1),        # Primary blue button
    'button_success': (0.2, 0.8, 0.2, 1),        # Green button
    'button_warning': (0.9, 0.6, 0.1, 1),        # Orange button
    'button_danger': (0.8, 0.2, 0.2, 1),         # Red button
    'medical_blue': (0.2, 0.6, 0.8, 1),          # Medical blue theme
}

def get_text_color_for_background(background_color):
    """
    Determine appropriate text color based on background brightness
    """
    # Calculate perceived brightness
    r, g, b = background_color[:3]
    brightness = (r * 0.299 + g * 0.587 + b * 0.114)
    
    # Return appropriate text color
    if brightness > 0.5:
        return COLORS['text_on_light']  # Dark text on light background
    else:
        return COLORS['text_on_dark']   # Light text on dark background

def apply_color_scheme():
    """
    Apply the improved color scheme to Kivy widgets
    """
    return COLORS