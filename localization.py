import cv2
import numpy as np

def map_coord_to_lane(y_coord):
    if y_coord <= 139:
        return 0
    elif 140 <= y_coord <= 164:
        return 1
    elif 165 <= y_coord <= 190:
        return 2
    elif 191 <= y_coord <= 217:
        return 3
    elif 218 <= y_coord <= 245:
        return 4
    elif y_coord >= 246:
        return 5
    else:
        return None  # or some default value or raise an exception

def detect_colors(frame):
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    center_green = None
    center_pink = None

    # Define range of pink color in HSV
    lower_pink = np.array([163, 105, 160])  # Adjust values as needed
    upper_pink = np.array([183, 185, 240])  # Adjust values as needed

    # Define range of green color in HSV
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
    red_dot_pos_pink = 0
    red_dot_pos_green = 0

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
    if center_pink is None:
        center_pink = (0, 0)
    if center_green is None:
        center_green = (0, 0)

    return center_green, center_pink, frame

def find_positions(queue):
    # Change the index to your camera's index if needed
    cap = cv2.VideoCapture(1)
    print("Camera is open")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Your logic to find the positions of two items
        center_green, center_pink, _ = detect_colors(frame)
        xpos_1, ypos_1 = center_green  
        xpos_2, ypos_2 = center_pink
        if xpos_1 is None:
            xpos_1 = 0
            ypos_1 = 0
        if xpos_2 is None:
            xpos_2 = 0
            ypos_2 = 0

        # Try to put the positions in the queue without blocking
        try:
            if queue.full():
                queue.get_nowait()  # Remove the oldest item if the queue is full
            queue.put_nowait((xpos_1, ypos_1, xpos_2, ypos_2))
        except Exception as e:
            print(f"Queue operation failed: {e}")

        # Display the frame (for debugging purposes)
        # cv2.imshow('Frame', frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    # cv2.destroyAllWindows()
