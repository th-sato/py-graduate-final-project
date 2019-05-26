# Picar-V
STRAIGHT_ANGLE = 90

# Camera
VIDEO_CAPTURE = 0
VIDEO_NAME = "autonomous_car/static/output.avi"
LOG_FILE_NAME = "autonomous_car/static/log.txt"

# Controller
FUZZY_CONTROLLER = "Fuzzy"
PROPORCIONAL_CONTROLLER = "Proporcional"

# Network
HOST = '0.0.0.0'
PORT = 5000
# URL_REDIS_IMAGE = 'http://192.168.1.189:8081/redis-image'
# KEY_JSON_IMAGE = "image"

# Image to show
STREET_ORIGINAL_IMAGE = 0
STREET_DETECTING = 1
STREET_LINES_DRAWN = 2

# Image dimensions
WIDTH_IMAGE = 432   # Pixels
HEIGHT_IMAGE = 240  # Pixels
# WIDTH_IMAGE = 432.0   # Pixels
# HEIGHT_IMAGE = 240.0  # Pixels

# Lane dimension
# WIDTH_LANE = 22.0           # Centimeters
# WIDTH_LANE_PIXEL = 350      # Pixels
# HEIGHT_LANE = 100.0         # Centimeters
# HEIGHT_LANE_PIXEL = 195     # Pixels
WIDTH_LANE = 0.22           # Meters
WIDTH_LANE_PIXEL = 350      # Pixels
HEIGHT_LANE = 1.0           # Meters
HEIGHT_LANE_PIXEL = 195     # Pixels

# Measures
AXIS_X_METERS_PER_PIXEL = WIDTH_LANE/WIDTH_LANE_PIXEL
AXIS_Y_METERS_PER_PIXEL = HEIGHT_LANE/HEIGHT_LANE_PIXEL


# Color to detect
DETECT_YELLOW = 0
DETECT_BLACK = 1

# Colors
WHITE = 255
BLACK = 0
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 70, 0]
