import cv2
import numpy as np

# 1 bounding box

# Function to detect neon green objects
def detect_neon_green(frame):
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of neon green color in HSV
    lower_green = np.array([60, 100, 100])
    upper_green = np.array([100, 255, 255])

    # Threshold the HSV image to get only neon green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables for bounding box and center dot
    bounding_box = None
    center = None

    # Loop through contours
    for contour in contours:
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h

        # Consider the largest bounding box
        if bounding_box is None or area > bounding_box[2] * bounding_box[3]:
            bounding_box = (x, y, w, h)
            center = (x + w // 2, y + h // 2)

    # Draw bounding box around the largest detected object
    if bounding_box is not None:
        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)  # Draw dot at the center

    return frame

# Main function
def main():
    # Open video capture
    cap = cv2.VideoCapture(0)  # Change the argument to the appropriate index if you have multiple cameras

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Call function to detect neon green objects
        result = detect_neon_green(frame)

        # Display the result
        cv2.imshow('Neon Green Detection', result)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
