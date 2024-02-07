import cv2
import time

WAIT_TIME = 2
AREA_THRESHOLD = 1000

class Camera_Sensor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.paper_detected = False
        self.paper_start_time = None

    def detect_paper(self, frame):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over the contours
        for contour in contours:
            # Calculate contour area
            area = cv2.contourArea(contour)

            # Approximate contour to a polygon
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            # Draw contours on the frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

            # Check if contour is approximately rectangular and has certain area
            if len(approx) == 4 and area > AREA_THRESHOLD:
                return True, contour
            
        return False, None
    
    def save_paper_image(self, frame, contour):
        # threshold the image
        _, thresh = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)

        # display the thresholded image
        cv2.imshow('Thresholded Image', thresh)
        # wait for user to press enter
        cv2.waitKey(0)

        # Extract and save the paper region as an image
        x, y, w, h = cv2.boundingRect(contour)
        paper_image = thresh[y:y+h, x:x+w]
        cv2.imwrite("paper_image.png", paper_image)
        print("Paper captured and saved")

    def capture_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        if not ret:
            print("Error: Could not capture frame")
            return None

        return frame
    
    def detect_paper_loop(self):
        while True:
            # Capture frame
            frame = self.capture_frame()
            frame_copy = frame.copy()

            # Detect paper in the frame
            detected, contour = self.detect_paper(frame)
            if detected:
                if not self.paper_detected:
                    self.paper_start_time = time.time()
                    self.paper_detected = True
                    print("Paper detected")

                if time.time() - self.paper_start_time >= WAIT_TIME:
                    # Calculate the angle of rotation of the contour
                    rect = cv2.minAreaRect(contour) # returns ((x, y), (w, h), angle)
                    angle = rect[-1]
                    if angle < -45:
                        angle = -(90 + angle)  # Rotate clockwise for negative angles
                    elif angle > 45:
                        angle = -(90 - angle)  # Rotate clockwise for positive angles

                    # Rotate the image to correct the orientation
                    (h, w) = frame.shape[:2]
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    rotated_frame = cv2.warpAffine(frame_copy, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                    rotated_frame = cv2.resize(rotated_frame, (w, h))
                    rotated_contour = cv2.transform(contour, M)
                    
                    cv2.imshow('Rotated Frame', rotated_frame)

                    self.save_paper_image(rotated_frame, rotated_contour)
                    break

            else:
                self.paper_detected = False

            # Display the frame
            cv2.imshow('Camera Stream', frame)

            # Exit loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    camera = Camera_Sensor()
    camera.detect_paper_loop()


