import cv2
import numpy as np

# Define standard letter paper size in pixels (300 DPI)
letter_paper_width = 2550  # 8.5 inches * 300 DPI
letter_paper_height = 3300  # 11 inches * 300 DPI
canvas_size = (letter_paper_width, letter_paper_height, 3)

# Create a white canvas
canvas = 255 * np.ones(canvas_size, dtype=np.uint8)

# Draw the grid
for i in range(1, 16):
    # Draw horizontal lines
    cv2.line(canvas, (0, i * (canvas_size[1] // 16)), (canvas_size[0], i * (canvas_size[1] // 16)), (0, 0, 0), 1)

    # Draw vertical lines
    cv2.line(canvas, (i * (canvas_size[0] // 16), 0), (i * (canvas_size[0] // 16), canvas_size[1]), (0, 0, 0), 1)

# Save the grid as an image
cv2.imwrite('maze_grid_template_letter_paper.png', canvas)

# Display the grid
cv2.imshow('Maze Grid Template (Letter Paper)', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()
