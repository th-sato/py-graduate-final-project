# Picar-V
STRAIGHT_ANGLE = 90

# Camera
VIDEO_CAPTURE = 0

# Controller
FUZZY_CONTROLLER = "Fuzzy"
PROPORCIONAL_CONTROLLER = "Proporcional"

# Network
HOST = '0.0.0.0'
PORT = 5000

# Image dimensions
# WIDTH_IMAGE = 432   # Pixels
# HEIGHT_IMAGE = 240  # Pixels

# Lane dimension
WIDTH_LANE = 22.0           # Centimeters
WIDTH_LANE_PIXEL = 350      # Pixels
HEIGHT_LANE = 100.0         # Centimeters
HEIGHT_LANE_PIXEL = 195     # Pixels

# Measures
AXIS_X_METERS_PER_PIXEL = WIDTH_LANE/WIDTH_LANE_PIXEL
AXIS_Y_METERS_PER_PIXEL = HEIGHT_LANE/HEIGHT_LANE_PIXEL

# Colors
WHITE = 255
BLACK = 0
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 70, 0]
