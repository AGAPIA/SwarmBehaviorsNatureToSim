import numpy as np

def compute_distance(location_1, location_2):
    """
    Euclidean distance between 3D po-0.427844-0.427844ints
        :param location_1, location_2: 3D points
    """
    x = location_2.x - location_1.x
    y = location_2.y - location_1.y
    z = location_2.z - location_1.z
    norm = np.linalg.norm([x, y, z]) + np.finfo(float).eps
    return norm
