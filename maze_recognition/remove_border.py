"""
Program should take in the image paper_image.png, and remove the border around the maze.
"""
import cv2

def remove_maze_border(input_image, output_image):
    # Load the image
    img = cv2.imread(input_image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the two parallel vertical contour lines which are approximately the same length
    lengths = []
    for contour in contours:
        # Calculate contour area
        area = cv2.contourArea(contour)

        # Approximate contour to a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # Check if contour is approximately rectangular and has certain area
        if len(approx) > 4 and area > 1000:
            # Draw contours on the frame
            cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
            lengths.append(approx)

    cv2.imshow('Image with contours', img)
    cv2.waitKey(0)

    # Crop the image to the region of the maze
    min_x = 10000
    max_x = 0
    min_y = 10000
    max_y = 0
    for contour in lengths:
        for point in contour:
            x = point[0][0]
            y = point[0][1]
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    # Crop the image
    img = img[min_y:max_y, min_x:max_x]

    # Set non-white pixels to black
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not all(channel > 240 for channel in img[i][j]):
                img[i][j] = [0, 0, 0]

    # Set the first and last 5 columns to black
    for i in range(img.shape[0]):
        for j in range(5):
            img[i][j] = [0, 0, 0]
            img[i][img.shape[1] - 1 - j] = [0, 0, 0]

    # # Display the cropped image
    # cv2.imshow('Cropped Image', img)
    # cv2.waitKey(0)

    # Save the cropped image
    cv2.imwrite(output_image, img)

    return 0

if __name__ == "__main__":
    remove_maze_border("paper_image.png", "cropped_maze.png")