import random
from vCam import *

## CHANGE exampleMovement to your file
from exampleMovement import *


def main():
    # Generate a random position
    pos = [random.randint(-3, 3), random.randint(-3, 3), random.randint(1, 5)]
    
    # Generate a 0 rotation or a random rotation
    rotation = 0                                  # Rotation in degrees
    ## rotation = random.randint(0, 360)           # Random Rotation in degrees (More Difficult)

    # Set the new position
    set_pos(pos, rotation)
    
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulate OpenCV processing by capturing the virtual camera frame
        frame = get_virtual_camera_frame()
        lineValues = findLine(frame)

        # Handle user input for movement
        handle_keyboard_input()

        # User movement controls
        # passed (vx, vy, x, y), width, height, camera_rotation
        tick(lineValues, WIDTH, HEIGHT, camera_rotation)

        # Render the scene
        render_scene()

        # Limit the frame rate to 30 FPS
        # Change for faster or slower
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()