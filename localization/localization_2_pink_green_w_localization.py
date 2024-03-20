import cv2
import numpy as np

# Function to detect pink, green, and red objects
def detect_colors(frame):
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of pink color in HSV
    lower_pink = np.array([150, 50, 50])  # Adjust values as needed
    upper_pink = np.array([170, 255, 255])  # Adjust values as needed

    # Define range of green color in HSV
    lower_green = np.array([60, 100, 100])  # Adjust values as needed
    upper_green = np.array([80, 255, 255])  # Adjust values as needed
    
    # Define range of red color in HSV
    lower_red1 = np.array([0, 100, 100])  # Adjust values as needed
    upper_red1 = np.array([10, 255, 255])  # Adjust values as needed
    lower_red2 = np.array([170, 100, 100])  # Adjust values as needed
    upper_red2 = np.array([180, 255, 255])  # Adjust values as needed

    # Threshold the HSV image to get only pink colors
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Threshold the HSV image to get only red colors
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Combine the masks
    combined_mask = cv2.bitwise_or(mask_pink, mask_green, mask_red)

    # Find contours in the combined mask
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variable to store red dot position
    red_dot_pos = None

    # Sort contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    # Draw bounding boxes around the detected objects
    for contour in contours:
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate center coordinates
        center = (x + w // 2, y + h // 2)
        # Draw dot at the center
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # If the object is red, update red dot position
        if np.array_equal(frame[center[1], center[0]], [0, 0, 255]):
            red_dot_pos = center

    # If red dot position is found, print its coordinates
    if red_dot_pos:
        print("Red Dot Position (x, y):", red_dot_pos)

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

        # Call function to detect pink, green, and red objects
        result = detect_colors(frame)

        # Display the result
        cv2.imshow('Pink, Green, and Red Detection', result)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
