import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 400
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ARROW_LENGTH = 150

# Create the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Compass")

def calculate_angle(height, width):
    # Calculate the angle in radians using arctangent
    angle_radians = math.atan2(height, width)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Set 0 to North
    # angle_degrees += 180
    # angle_degrees += 180
    # angle_degrees += 90

    # Keep in Quadrants 1 & 2
    angle_degrees += 180 if (angle_degrees < 90) else 0

    # Ensure the angle is between 0 and 360 degrees
    angle_degrees = (angle_degrees + 360) % 360

    return angle_degrees

def draw_compass(angle_degrees):
    pygame.display.set_caption(f"Compass at: {angle_degrees} degrees")
    screen.fill(WHITE)

    # Draw the compass circle
    pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), 150)

    # Draw the arrow
    angle_radians = math.radians(angle_degrees - 90)
    arrow_end_x = CENTER_X + ARROW_LENGTH * math.cos(angle_radians)
    arrow_end_y = CENTER_Y - ARROW_LENGTH * math.sin(angle_radians)
    pygame.draw.line(screen, RED, (CENTER_X, CENTER_Y), (arrow_end_x, arrow_end_y), 5)

    pygame.display.update()

def display_compass(angle):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_compass(angle)

    pygame.quit()
