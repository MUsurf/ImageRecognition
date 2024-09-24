from vCam import *

# CHANGE exampleMovement to your file
from exampleMovement import *

def main():
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input for movement
        handle_keyboard_input()
        tick()

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