import cv2
import time
import pytesseract


def monitor():
    # looping behavior state, sentry mode or target acquired
    print("Monitor Booting...")
    time.sleep(1)

    # Load the image with the blue line
    lines_image = cv2.imread('lines_image.jpg')

    # Keep looking for image
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error reading frame")
            break

        # Rotate the image 90 degrees ccw
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        # Resize image
        resized_frame = cv2.resize(rotated_frame, (800, 800))

        # Overlay the lines image onto the resized frame
        combined_frame = cv2.addWeighted(resized_frame, 1, lines_image, 0.5, 0)

        cv2.imshow('Live', combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # End
    print("...Monitor Closing")


# Global variable to store captured frame
captured_frame = None

def process_image():
    global captured_frame

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret or frame is None:
            print("Error reading frame")
            break

        # Rotate and resize the frame
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.resize(frame, (800, 800))

        # Preprocess the image
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Display the thresholded image
        cv2.imshow('Thresholded Image', binary_frame)

        # Check for key press
        key = cv2.waitKey(1)

        # If Enter key is pressed, capture the frame and process it
        if key == 13:  # 13 is the ASCII code for Enter key
            # Store the captured frame
            captured_frame = frame.copy()

            # Create lines for all black pixels surrounded by other black pixels
            lines_image = captured_frame.copy()
            for y in range(1, lines_image.shape[0] - 1):
                for x in range(1, lines_image.shape[1] - 1):
                    if binary_frame[y, x] == 0 and binary_frame[y-1:y+2, x-1:x+2].sum() == 0:
                        cv2.line(lines_image, (x, y), (x, y), (255, 0, 0), thickness=1)  # Draw blue lines

            # Save the image with lines
            cv2.imwrite('lines_image.jpg', lines_image)
            print("Image with lines saved as lines_image.jpg")

        # If 'q' key is pressed, exit the loop
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_image()
