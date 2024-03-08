import cv2
import numpy as np

# Function to detect neon green objects
def detect_neon_green(image):
    # Convert image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of neon green color in HSV
    lower_green = np.array([60, 100, 100])
    upper_green = np.array([100, 255, 255])

    # Threshold the HSV image to get only neon green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding box around detected objects
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return image

# Main function
def main():
    # Read input image
    image = cv2.imread('your_image_path.jpg')  # Change 'your_image_path.jpg' to the path of your input image

    # Call function to detect neon green objects
    result = detect_neon_green(image)

    # Display the result
    cv2.imshow('Neon Green Detection', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()