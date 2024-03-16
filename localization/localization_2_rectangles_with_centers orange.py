import cv2
import numpy as np

#Orange works well

# Function to detect regular orange objects
def detect_orange(frame):
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of regular orange color in HSV
    lower_orange = np.array([5, 100, 100])  # Adjust values as needed
    upper_orange = np.array([20, 255, 255])  # Adjust values as needed

    # Threshold the HSV image to get only regular orange colors
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    # Draw bounding boxes around the two largest detected objects
    for contour in contours:
        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate center coordinates
        center = (x + w // 2, y + h // 2)
        # Draw dot at the center
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

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

        # Call function to detect regular orange objects
        result = detect_orange(frame)

        # Display the result
        cv2.imshow('Regular Orange Detection', result)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
