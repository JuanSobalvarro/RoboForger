from math import tau, pi

import os
import sys
from pathlib import Path


def real_coord2robo_coord(vx: tuple[float, float, float], trans: tuple[float, float, float] = (450, 0, 350)) -> tuple[float, float, float]:

    if not isinstance(vx, tuple):
        raise TypeError("Input must be a tuple of (x, y, z) coordinates: ", vx)

    return vx[0] + trans[0], vx[1] + trans[1], vx[2] + trans[2]

def normalize_coordinates(
    coordinates: tuple,
    origin: tuple = (0.0, 0.0, 0.0),
    corners: tuple[tuple, tuple] = ((-810, -810, 0), (-810, -810, 0))
) -> tuple:
    """
    Normalize a coordinate to a new origin based on the workspace corners.

    Parameters:
        coordinates (tuple): The (x, y, z) coordinate to normalize.
        origin (tuple): The desired origin in robot space.
        corners (tuple): ((min_x, min_y, min_z), (max_x, max_y, max_z)) defining the workspace bounding box.

    Returns:
        tuple: The normalized (x, y, z) coordinate.
    """
    (min_x, min_y, min_z), _ = corners

    # Calculate offset to move min workspace corner to desired origin
    offset = (
        origin[0] - min_x,
        origin[1] - min_y,
        origin[2] - min_z
    )

    # Apply offset to the coordinate
    normalized = (
        coordinates[0] + offset[0],
        coordinates[1] + offset[1],
        coordinates[2] + offset[2]
    )

    return normalized


def export_str2txt(s: str, filepath: str) -> None:
    # If filename exists, it will be overwritten.
    if not filepath.endswith('.txt'):
        filepath += '.txt'
    with open(filepath, "w") as file:
        file.write(s)
    print(f"Exported to {filepath} successfully.")

def round_tuple(t: tuple, precision: int = 2) -> tuple:
    """
    Round each element of a tuple to the specified precision.

    Parameters:
        t (tuple): The tuple to round.
        precision (int): The number of decimal places to round to.

    Returns:
        tuple: A new tuple with rounded values.
    """
    return tuple(round(x, precision) for x in t)


def normalize_angle(angle_rad: float) -> float:
    """
    Normalize any angle in radians to the range [0, 2π).

    Args:
        angle_rad (float): Angle in radians.

    Returns:
        float: Normalized angle in radians, in [0, 2π).
    """
    return angle_rad % tau


def normalize_angle_deg(angle_deg: float) -> float:
    """
    Normalize any angle in degrees to the range [0, 360).

    Args:
        angle_deg (float): Angle in degrees.

    Returns:
        float: Normalized angle in degrees, in [0, 360).
    """
    return angle_deg % 360

def vector_norm(vector: tuple[float, float, float]) -> float:
    """
    Calculate the Euclidean norm (magnitude) of a 3D vector.

    Args:
        vector (tuple[float, float, float]): The 3D vector as a tuple of (x, y, z).

    Returns:
        float: The magnitude of the vector.
    """
    return sum(coord ** 2 for coord in vector) ** 0.5

def distance_vectors(vector1: tuple[float, float, float], vector2: tuple[float, float, float]) -> float:
    """
    Calculate the Euclidean distance between two 3D vectors.

    Args:
        vector1 (tuple[float, float, float]): The first vector.
        vector2 (tuple[float, float, float]): The second vector.

    Returns:
        float: The distance between the two vectors.
    """
    return vector_norm(tuple(v1 - v2 for v1, v2 in zip(vector1, vector2)))

def get_resources_dir() -> Path:
    if "__compiled__" in globals():
        # nuitka Resources are next to the executable
        base_dir = Path(sys.executable).parent
    else:
        # Standard Python Resources are relative to this file, remember that if resources folder are moved or missing, this will break
        base_dir = Path(__file__).resolve().parent

    resource_dir = base_dir / "resources"

    if not resource_dir.exists():
        raise FileNotFoundError(
            f"Resource dir missing.\n"
            f"Expected at: {resource_dir}\n"
            f"Base dir was: {base_dir}\n"
            f"Is Compiled: {'__compiled__' in globals()}"
        )

    return resource_dir

def get_resource_path(relative_path: str) -> str:
    resource_dir = get_resources_dir()
    return os.path.join(resource_dir, relative_path)