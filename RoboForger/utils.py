from math import tau, pi

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


def export_str2txt(s: str, filename: str) -> None:
    # If filename exists, it will be overwritten.
    if not filename.endswith('.txt'):
        filename += '.txt'
    with open(filename, "w") as file:
        file.write(s)
    print(f"Exported to {filename} successfully.")

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
