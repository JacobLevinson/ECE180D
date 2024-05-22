import cv2
import numpy as np

def detect_colors(frame):
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of pink color in HSV
    lower_pink = np.array([150, 50, 50])  # Adjust values as needed
    upper_pink = np.array([170, 255, 255])  # Adjust values as needed

    # Define range of green color in HSV
    # Green is Yellow in Practice
    lower_green = np.array([25, 80, 200])  # Adjust values as needed
    upper_green = np.array([50, 170, 255])  # Adjust values as needed
    
    # Threshold the HSV image to get only pink colors
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)

    # Threshold the HSV image to get only green colors
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the pink mask
    contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find contours in the green mask
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables to store red dot positions
    red_dot_pos_pink = None
    red_dot_pos_green = None

    # Process pink contours
    if contours_pink:
        # Sort contours by area in descending order
        contours_pink = sorted(contours_pink, key=cv2.contourArea, reverse=True)
        # Get the largest contour (bounding box) for pink
        x_pink, y_pink, w_pink, h_pink = cv2.boundingRect(contours_pink[0])
        # Calculate center coordinates for pink
        center_pink = (x_pink + w_pink // 2, y_pink + h_pink // 2)
        # Draw bounding box for pink
        cv2.rectangle(frame, (x_pink, y_pink), (x_pink + w_pink, y_pink + h_pink), (255, 0, 255), 2)
        # Draw red dot at the center for pink
        cv2.circle(frame, center_pink, 5, (0, 0, 255), -1)
        red_dot_pos_pink = center_pink

    # Process green contours
    if contours_green:
        # Sort contours by area in descending order
        contours_green = sorted(contours_green, key=cv2.contourArea, reverse=True)
        # Get the largest contour (bounding box) for green
        x_green, y_green, w_green, h_green = cv2.boundingRect(contours_green[0])
        # Calculate center coordinates for green
        center_green = (x_green + w_green // 2, y_green + h_green // 2)
        # Draw bounding box for green
        cv2.rectangle(frame, (x_green, y_green), (x_green + w_green, y_green + h_green), (255, 255, 0), 2)
        # Draw red dot at the center for green
        cv2.circle(frame, center_green, 5, (0, 0, 255), -1)
        red_dot_pos_green = center_green

    # If red dot positions are found, print their coordinates
    # if red_dot_pos_pink:
    #     print("Pink Dot Position (x, y):", red_dot_pos_pink)
    if red_dot_pos_green:
        print("Green Dot Position (x, y):", red_dot_pos_green)

    return frame

# Main function
def main():
    # Open video capture
    cap = cv2.VideoCapture(1)  # Change the argument to the appropriate index if you have multiple cameras

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Call function to detect pink and green objects
        result = detect_colors(frame)

        # Display the result
        cv2.imshow('Pink and Green Detection', result)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
