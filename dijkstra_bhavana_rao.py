
import pygame
import math
from queue import PriorityQueue
import time

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 1200, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dijkstra')

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)  # For the obstacle space
red = (255, 0, 0)  # For the clearance
blue = (230, 230, 250)

# Function to draw a regular hexagon
# Hexagon parameters
edge_length_ncl = 150
edge_length = 155.88

# Center of the hexagon
cx, cy = 650, 250

# Parameters
edge_length = 150  # Side length of the hexagon
clearance = 5  # Additional space around the hexagon
edge_length = 150  # side length of the hexagon
cx, cy = 650, 250  # center of the hexagon
angles = [30, 90, 150, 210, 270, 330]  # angles for vertices from the top

# Calculate the hexagon vertices without clearance
hexagon_points_no_clearance = [
    (cx + edge_length_ncl * math.cos(math.radians(angle)), cy + edge_length_ncl * math.sin(math.radians(angle)))
    for angle in angles
]


# Calculate the hexagon vertices with clearance
hexagon_points = [
    (cx + (edge_length + clearance) * math.cos(math.radians(angle)), cy + (edge_length + clearance) * math.sin(math.radians(angle)))
    for angle in angles
]


def point_inside_hexagon(x, y, hexagon_points):
    """
    Check if a point (x, y) lies inside a hexagon defined by its vertices.
    """
    num_vertices = len(hexagon_points)
    inside = False
    p1x, p1y = hexagon_points[0]
    for i in range(num_vertices + 1):
        p2x, p2y = hexagon_points[i % num_vertices]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def get_valid_input(prompt):
    while True:
        try:
            x = int(input(prompt + " X coordinate: "))
            y = int(input(prompt + " Y coordinate: "))
            y = height - y
            if not (0 <= x <= 1200 and 0 <= y <= 500):
                raise ValueError("Coordinates out of bounds")
            elif point_inside_hexagon(x, y, hexagon_points):
                raise ValueError("Coordinates within hexagon obstacle space")
            elif (100 - 5 <= x <= 175 + 5 and 0 <= y <= 400 + 5) or \
                 (275 - 5 <= x <= 350 + 5 and 100 - 5 <= y <= 500) or \
                 (900 - 5 <= x <= 1100 + 5 and 50 - 5 <= y <= 125 + 5) or \
                 (1020 - 5 <= x <= 1100 + 5 and 50 - 5 <= y <= 450 + 5) or \
                 (900 - 5 <= x <= 1100 + 5 and 375 - 5 <= y <= 450 + 5) or \
                 (0 <= x <= 5 and 0 <= y <= height) or \
                 (0 <= x <= width and 0 <= y <= 5) or \
                 (width - 5 <= x <= width and 0 <= y <= height) or \
                 (0 <= x <= width and height - 5 <= y <= height):
                raise ValueError("Coordinates within obstacle space")
            return x, y  # Adjust y-coordinate
        except ValueError as e:
            print("Invalid input:", e)

# Rest of the code remains unchanged
def move_right(node):
    return node[0] + 1, node[1]


def move_left(node):
    return node[0] - 1, node[1]


def move_up(node):
    return node[0], node[1] + 1


def move_down(node):
    return node[0], node[1] - 1


def move_diagonal_up_right(node):
    return node[0] + 1, node[1] + 1


def move_diagonal_up_left(node):
    return node[0] - 1, node[1] + 1


def move_diagonal_down_right(node):
    return node[0] + 1, node[1] - 1


def move_diagonal_down_left(node):
    return node[0] - 1, node[1] - 1


# Action set
actions = [move_right, move_left, move_up, move_down,
           move_diagonal_up_right, move_diagonal_up_left,
           move_diagonal_down_right, move_diagonal_down_left]

# Take start and end points from user
start_point = get_valid_input("Enter start")
end_point = get_valid_input("Enter end")

# Generate the graph
graph = [[] for _ in range(width * height)]
goal_reached = False  # Flag to track if the goal point is reached
for x in range(width):
    if goal_reached:  # If the goal point is reached, break out of the loop
        break
    for y in range(height):
        node_index = y * width + x
        if goal_reached:
            break  # Break out of the outer loop if the goal point is reached

        if point_inside_hexagon(x, y, hexagon_points):
            continue  # Skip generating connections for points within the hexagon obstacle

        if (100 - 5 <= x <= 175 + 5 and 0 <= y <= 400 + 5) or \
                (275 - 5 <= x <= 350 + 5 and 100 - 5 <= y <= 500) or \
                (900 - 5 <= x <= 1100 + 5 and 50 - 5 <= y <= 125 + 5) or \
                (1020 - 5 <= x <= 1100 + 5 and 50 - 5 <= y <= 450 + 5) or \
                (900 - 5 <= x <= 1100 + 5 and 375 - 5 <= y <= 450 + 5) or \
                (0 <= x <= 5 and 0 <= y <= height) or \
                (0 <= x <= width and 0 <= y <= 5) or \
                (width - 5 <= x <= width and 0 <= y <= height) or \
                (0 <= x <= width and height - 5 <= y <= height):
            continue  # Skip generating connections for points within the rectangle obstacles

        for action in actions:
            new_x, new_y = action((x, y))
            if 0 <= new_x < width and 0 <= new_y < height:
                new_node_index = new_y * width + new_x
                if point_inside_hexagon(x, y, hexagon_points):
                    continue  # Skip generating connections for points within the hexagon obstacle

                if (100 - 5 <= new_x <= 175 + 5 and 0 <= new_y <= 400 + 5) or \
                        (275 - 5 <= new_x <= 350 + 5 and 100 - 5 <= new_y <= 500) or \
                        (900 - 5 <= new_x <= 1100 + 5 and 50 - 5 <= new_y <= 125 + 5) or \
                        (1020 - 5 <= new_x <= 1100 + 5 and 50 - 5 <= new_y <= 450 + 5) or \
                        (900 - 5 <= new_x <= 1100 + 5 and 375 - 5 <= new_y <= 450 + 5) or \
                        (0 <= new_x <= 5 and 0 <= new_y <= height) or \
                        (0 <= new_x <= width and 0 <= new_y <= 5) or \
                        (width - 5 <= new_x <= width and 0 <= new_y <= height) or \
                        (0 <= new_x <= width and height - 5 <= new_y <= height):
                    continue  # Skip generating connections for points within the rectangle obstacles

                graph[node_index].append(new_node_index)

                if (new_x, new_y) == end_point:  # Check if the new node is the goal point
                    goal_reached = True  # Set the flag to indicate that the goal point is reached
                    break  # Break out of the loop if the goal point is reached
        if goal_reached:
            break  # Break out of the outer loop if the goal point is reached


def dijkstra(graph, start_index, end_index):
    pq = PriorityQueue()
    pq.put((0, start_index, []))  # Cost from start to node, current node, path of nodes
    visited = set()
    parents = {start_index: None}  # To reconstruct the path later

    while not pq.empty():
        (dist, current_node_index, path) = pq.get()
        if current_node_index in visited:
            continue
        visited.add(current_node_index)

        # Visualize node exploration
        current_x = current_node_index % width
        current_y = current_node_index // width
        current_node = (current_x, current_y)
        if current_node != start_point:  # Avoid redrawing the start node
            pygame.draw.circle(screen, blue, current_node, 2)
            pygame.display.update()

        if current_node == end_point:  # If end node is reached
            final_path = []
            while current_node_index is not None:
                final_path.append((current_node_index % width, current_node_index // width))
                current_node_index = parents[current_node_index]
            final_path.reverse()
            return final_path  # Return reversed path from start to end

        for neighbor_index in graph[current_node_index]:
            if neighbor_index not in visited:
                new_cost = dist + 1  # Assuming cost of 1 for up, down, left, right
                if abs(neighbor_index - current_node_index) == width + 1 or \
                   abs(neighbor_index - current_node_index) == width - 1:  # Diagonal move
                    new_cost = dist + 1.4  # Approximately the square root of 2

                pq.put((new_cost, neighbor_index, path + [neighbor_index]))
                parents[neighbor_index] = current_node_index  # To reconstruct the path later

    return None  # If no path is found



# Main loop
running = True
should_terminate = False
clock = pygame.time.Clock()
path_drawn = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    start = time.time()
    # Fill the background with white color
    screen.fill((255, 255, 255))

    # Draw the rectangle with clearance
    pygame.draw.rect(screen, green, (100 - 5, 0 - 5, 75 + 10, 400 + 10))  # Left vertical
    pygame.draw.rect(screen, green, (275 - 5, 100 - 5, 75 + 10, 400 + 10))  # Right vertical
    pygame.draw.rect(screen, green, (900 - 5, 50 - 5, 200 + 10, 75 + 10))  # Bottom horizontal
    pygame.draw.rect(screen, green, (1020 - 5, 50 - 5, 80 + 10, 400 + 10))  # Right vertical small
    pygame.draw.rect(screen, green, (900 - 5, 375 - 5, 200 + 10, 75 + 10))  # Top horizontal

    # Draw the hexagon with clearance
    pygame.draw.polygon(screen, green, hexagon_points)

    # Draw the rectangle without clearance (red color)
    pygame.draw.rect(screen, red, (100, 0, 75, 400))  # Left vertical
    pygame.draw.rect(screen, red, (275, 100, 75, 400))  # Right vertical
    pygame.draw.rect(screen, red, (900, 50, 200, 75))  # Bottom horizontal
    pygame.draw.rect(screen, red, (1020, 50, 80, 400))  # Right vertical small
    pygame.draw.rect(screen, red, (900, 375, 200, 75))  # Top horizontal

    # Draw the hexagon without clearance (red color)
    pygame.draw.polygon(screen, red, hexagon_points_no_clearance)

    # Draw the lines at 5mm distance from each corner
    # Draw the lines and fill the areas with green
    pygame.draw.rect(screen, green, (0, 0, 5, height))  # Left line
    pygame.draw.rect(screen, green, (0, 0, width, 5))  # Top line
    pygame.draw.rect(screen, green, (width - 5, 0, 5, height))  # Right line
    pygame.draw.rect(screen, green, (0, height - 5, width, 5))  # Bottom line

    # Draw start and end points
    pygame.draw.circle(screen, black, start_point, 5)  # Start point
    pygame.draw.circle(screen, black, end_point, 5)  # End point

    if not path_drawn:
        path = dijkstra(graph, start_point[1] * width + start_point[0], end_point[1] * width + end_point[0])
        if path:
            for x, y in path:
                pygame.draw.circle(screen, black, (x, y), 2)
                pygame.display.update()  # Update the display with the new path
        else:
            print("No path found from", start_point, "to", end_point)
        path_drawn = True
        should_terminate = True  # Set the flag to terminate the program
    pygame.display.flip()

    pygame.time.delay(5000)  # Control frame rate

    end = time.time()
    print(end-start)


pygame.quit()

