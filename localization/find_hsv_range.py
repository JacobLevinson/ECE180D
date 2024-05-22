import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the image
image_path = 'hat_pink.png'  # Replace with your image path
image = cv2.imread(image_path)

# Convert to HSV color space
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Display the image to select a pixel
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Select a pixel from the pink hat")
plt.show()

# Manually selected pixel (adjust these coordinates based on visual inspection)
selected_pixel = hsv_image[40, 50]  # Example coordinates, adjust as needed

# Define the range around the selected pixel's HSV values
hue_variation = 10
saturation_variation = 40
value_variation = 40

lower_hsv = np.array([selected_pixel[0] - hue_variation, max(0, selected_pixel[1] - saturation_variation), max(0, selected_pixel[2] - value_variation)])
upper_hsv = np.array([selected_pixel[0] + hue_variation, min(255, selected_pixel[1] + saturation_variation), min(255, selected_pixel[2] + value_variation)])

print("Lower HSV:", lower_hsv)
print("Upper HSV:", upper_hsv)

# Create a mask using the HSV range
mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)

# Apply the mask to the original image
result = cv2.bitwise_and(image, image, mask=mask)

# Display the result
cv2.imshow('Original Image', image)
cv2.imshow('Mask', mask)
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
