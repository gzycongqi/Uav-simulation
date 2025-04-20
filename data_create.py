def parse_beam_search_solution(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parse coordinates
    coordinates = []
    for line in lines[1:51]:  # Assuming coordinates are in lines 2 to 51
        x, y = map(float, line.strip().split(','))
        coordinates.append((x, y))

    # Parse indices
    indices = []
    for line in lines[52:]:  # Assuming indices start from line 53
        indices.append(int(line.strip()))

    return coordinates, indices

# Example usage
file_path = 'beam_search_solution.txt'
coordinates, indices = parse_beam_search_solution(file_path)

# Reorder and scale the coordinates based on the indices
scale_factor = 1000  # Define your scale factor here
reordered_coordinates = [(scale_factor * coordinates[i][0], scale_factor * coordinates[i][1]) for i in indices]

# Print the reordered coordinates
print("Reordered Coordinates:")
print(reordered_coordinates)
