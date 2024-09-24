import pygame
import cv2
import numpy as np
import math
import random

import sys
sys.path.append('./orange_oblong_detection')
from orange_oblong_line_draw import *

# Initialize Pygame
pygame.init()

# Define screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define camera properties
camera_pos = [0, 0, 5]  # Start the camera a little away from the blob
camera_rotation = 0                                                                # Rotation in degrees

# Define the orange blob (ellipse)
orange_color = (255, 165, 0)
blob_width, blob_height = 50, 100

# Blob's initial position in world space (not relative to camera)
blob_pos = [0, 0]

# Define movement speed
move_speed = 0.05
rotate_speed = 0.5

# Pygame clock for controlling the frame rate
clock = pygame.time.Clock()

def set_pos(position, rotation):
    global camera_pos, camera_rotation
    camera_pos = position
    camera_rotation = rotation

def render_scene():
    # Clear screen with blue background
    screen.fill((0, 0, 255))  # Blue background to simulate the ocean

    # Calculate the relative position of the blob based on the camera's position
    rel_x = blob_pos[0] - camera_pos[0]
    rel_y = blob_pos[1] - camera_pos[1]
    distance = camera_pos[2]  # Simulate moving forward/backward with distance

    # Simulate size scaling as the camera moves forward/backward
    scaled_width = int(blob_width * (1 / distance))
    scaled_height = int(blob_height * (1 / distance))

    # Convert world coordinates to screen coordinates
    screen_x = WIDTH // 2 + int(rel_x * 100)  # Centered on screen, scaled to world units
    screen_y = HEIGHT // 2 + int(rel_y * 100)

    # Create a surface to draw the blob (ellipse) on
    blob_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
    pygame.draw.ellipse(blob_surface, orange_color, (0, 0, scaled_width, scaled_height))

    # Apply rotation to the blob surface around its center
    rotated_blob = pygame.transform.rotate(blob_surface, camera_rotation)

    # Get the new rect of the rotated blob to center it properly
    rotated_rect = rotated_blob.get_rect(center=(screen_x, screen_y))

    # Draw the rotated blob onto the screen
    screen.blit(rotated_blob, rotated_rect)

    # Display the virtual camera output on the screen
    pygame.display.flip()

def move_camera(forward=0, right=0, dz=0):
    global camera_pos

    # Calculate the angle in radians for the camera's rotation
    angle_rad = math.radians(camera_rotation)

    # Move forward/backward in the direction the camera is facing
    camera_pos[0] += -forward * math.sin(angle_rad) * move_speed
    camera_pos[1] += -forward * math.cos(angle_rad) * move_speed

    # Move left/right relative to the camera's current facing direction
    camera_pos[0] += right * math.cos(angle_rad) * move_speed
    camera_pos[1] -= right * math.sin(angle_rad) * move_speed

    # Adjust the camera's height (z-axis)
    camera_pos[2] += dz
    camera_pos[2] = max(camera_pos[2], 0.1)

    # Prevent the camera from getting too close (or going backward to a negative distance)
    # if camera_pos[2] < config['camera']['max_distance']:
    #     camera_pos[2] = config['camera']['max_distance']

def rotate_camera(degrees=0):
    global camera_rotation
    # Adjust camera rotation
    camera_rotation += degrees
    camera_rotation %= 360  # Keep the rotation angle within 0-360 degrees

def move_sub(forward, right, dz, degrees):
    move_camera(-(forward * move_speed), -(right * move_speed), (dz * move_speed))
    rotate_camera(degrees * rotate_speed)

def handle_keyboard_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        move_camera(right=-move_speed)  # Move left
    if keys[pygame.K_RIGHT]:
        move_camera(right=move_speed)  # Move right
    if keys[pygame.K_UP]:
        move_camera(forward=move_speed)  # Move down
    if keys[pygame.K_DOWN]:
        move_camera(forward=-move_speed)  # Move up
    if keys[pygame.K_w]:
        move_camera(dz=-move_speed)  # Move forward
    if keys[pygame.K_s]:
        move_camera(dz=move_speed)  # Move backward
    if keys[pygame.K_a]:
        rotate_camera(degrees=-rotate_speed)  # Rotate counter-clockwise
    if keys[pygame.K_d]:
        rotate_camera(degrees=rotate_speed)  # Rotate clockwise

def get_virtual_camera_frame():
    """ 
    Returns the current screen's pixel data as a format that can be used with OpenCV. 
    Useful to simulate the virtual camera view for image processing.
    """
    # Get the Pygame screen surface data
    raw_data = pygame.surfarray.array3d(screen)
    
    # Convert from (R, G, B) to (B, G, R) to be compatible with OpenCV
    frame = cv2.cvtColor(np.transpose(raw_data, (1, 0, 2)), cv2.COLOR_RGB2BGR)
    
    return frame

def main():
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input for movement
        handle_keyboard_input()

        # Render the scene
        render_scene()

        # Simulate OpenCV processing by capturing the virtual camera frame
        frame = get_virtual_camera_frame()
        findLine(frame)

        # Limit the frame rate to 30 FPS
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
