import cv2 as cv
import numpy as np

# ChatGPT function to combine frame and mask by darkening and desaturating areas not in mask
def blend_frame_with_mask(frame, mask, brightness_factor=0.5, saturation_factor=0.5):
    """
    Blend the original frame with a mask, lowering both brightness and saturation
    in areas outside the mask.
    
    :param frame: The original camera input frame (BGR).
    :param mask: A binary mask where the masked region should stay bright and saturated.
    :param brightness_factor: Factor to reduce brightness in the areas outside the mask (0 to 1).
    :param saturation_factor: Factor to reduce saturation in the areas outside the mask (0 to 1).
    :return: The combined frame with lowered brightness and saturation outside the mask.
    """
    # Ensure mask is single channel
    if len(mask.shape) > 2:
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
    
    # Convert frame from BGR to HSV
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Split the HSV channels
    h, s, v = cv.split(hsv_frame)

    # Darken the brightness and lower the saturation outside the mask
    mask_inv = cv.bitwise_not(mask)
    
    v_darkened = cv.bitwise_and(v, v, mask=mask_inv)
    v_darkened = (v_darkened * brightness_factor).astype(np.uint8)
    
    s_desaturated = cv.bitwise_and(s, s, mask=mask_inv)
    s_desaturated = (s_desaturated * saturation_factor).astype(np.uint8)

    # Merge the bright areas back into the original V and S channels
    v_combined = cv.add(v_darkened, cv.bitwise_and(v, v, mask=mask))
    s_combined = cv.add(s_desaturated, cv.bitwise_and(s, s, mask=mask))

    # Merge the channels back
    hsv_combined = cv.merge([h, s_combined, v_combined])

    # Convert back to BGR
    combined_frame = cv.cvtColor(hsv_combined, cv.COLOR_HSV2BGR)

    return combined_frame

# Example usage
if __name__ == "__main__":
    # Example frame from a camera (replace this with actual frame input)
    frame = cv.imread('camera_input.jpg')  # Load an example camera input

    # Create a dummy binary mask (replace this with your actual mask)
    lower_color = np.array([30, 30, 30])  # Define the lower color range
    upper_color = np.array([200, 200, 200])  # Define the upper color range
    mask = cv.inRange(frame, lower_color, upper_color)  # Generate a color mask

    # Blend the frame with the mask
    blended_frame = blend_frame_with_mask(frame, mask, brightness_factor=0.5, saturation_factor=0.5)

    # Display the result
    cv.imshow("Blended Frame", blended_frame)
    cv.waitKey(0)
    cv.destroyAllWindows()
