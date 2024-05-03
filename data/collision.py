import numpy as np 

def point_line_distance(point, start, end):
    point = np.array(point)
    start = np.array(start)
    end = np.array(end)

    # Vector from start to point and start to end
    line_vec = end - start
    point_vec = point - start

    # Calculate the projection scalar of point_vec onto line_vec
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    proj_length = np.dot(point_vec, line_unitvec)

    # Check if the projection length is within the line segment
    if proj_length < 0:
        # Before start point
        closest_point = start
    elif proj_length > line_len:
        # After end point
        closest_point = end
    else:
        # Projection point on the line
        closest_point = start + proj_length * line_unitvec

    # Distance from the point to the closest point on the line segment
    return np.linalg.norm(point - closest_point)

def calculate_normal(start, end):
    """Calculate a normal vector to the line defined by start and end points."""
    line_vec = np.array(end) - np.array(start)
    normal_vec = np.array([-line_vec[1], line_vec[0]])
    norm = np.linalg.norm(normal_vec)
    if norm == 0:
        return normal_vec  # Avoid division by zero
    return normal_vec / norm

def reflect(velocity, normal):
    """Reflect a velocity vector off a normal vector."""
    velocity = np.array(velocity)
    normal = np.array(normal)
    return velocity - 2 * np.dot(velocity, normal) * normal