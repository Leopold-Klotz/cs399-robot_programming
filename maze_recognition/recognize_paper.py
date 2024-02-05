"""
This is a script to recognize a paper in a frame and extract the paper's ROI.
"""


import cv2

# Global variables for ROI selection
roi_x, roi_y, roi_width, roi_height = -1, -1, -1, -1
selecting_roi = False

def select_roi(event, x, y, flags, param):
    global roi_x, roi_y, roi_width, roi_height, selecting_roi

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_x, roi_y = x, y
        selecting_roi = True
    elif event == cv2.EVENT_LBUTTONUP and selecting_roi:
        roi_width, roi_height = x - roi_x, y - roi_y
        selecting_roi = False

# Open a connection to the camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Prompt to capture a photo
input("Press Enter to capture a photo...")

# Capture a frame from the camera
ret, frame = cap.read()

# Check if the frame was captured successfully
if not ret:
    print("Error: Could not capture a frame.")
    exit()

# Display the captured frame
cv2.imshow('Capture', frame)

# Set up the callback function for ROI selection
cv2.setMouseCallback('Capture', select_roi)

# Wait for the user to select the ROI
while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q') or key == 27:  # 'q' or Esc key to exit
        break

# Print the selected ROI coordinates and size
print("ROI Coordinates and Size:")
print(f"X: {roi_x}, Y: {roi_y}")
print(f"Width: {roi_width}, Height: {roi_height}")

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
