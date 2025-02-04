import math
import numpy as np
from scipy.optimize import fsolve

def find_point(x0, r0, r1, theta):
    """
    Finds the point (xs, y0) that is equidistant from two points:
    A = (x0 + r0, y0) and B = (x0 + r1 * cos(theta), y0 + r1 * sin(theta)).

    Args:
    - x0 (float): The x-coordinate of the center point.
    - y0 (float): The y-coordinate of the center point.
    - r0 (float): The radius of the first circle centered at A.
    - r1 (float): The radius of the second circle centered at B.
    - theta (float): The angle in radians between the x-axis and the line from the center point to point B.

    Returns:
    - (float, float): The x-coordinate of the point xs and the distance from this point to A and B, rounded to the nearest integer.
    """

    # Function to calculate the distance from xs to points A and B
    def equations(xs):
        dist_A = abs(xs - (x0 + r0))
        dist_B = np.sqrt((xs - (x0 + r1 * np.cos(theta))) ** 2 + (r1 * np.sin(theta)) ** 2)
        return dist_A - dist_B

    xs_initial_guess = (x0 + r0 + (x0 + r1 * np.cos(theta))) / 2
    xs_solution = fsolve(equations, xs_initial_guess)

    # If fsolve returns a result as an array, we extract the first value
    if not isinstance(xs_solution, np.ndarray):
        xs_solution = np.array([xs_solution])
    xs_solution = xs_solution[0]

    distance = abs(xs_solution - (x0 + r0))

    return xs_solution, distance


def generate_points(x0, y0, r0, r1, theta, n):
    """
    Generates n points on a circle centered at (xs, y0) with radius `distance`,
    where the first point is at B and the last point is at B' (the reflection of B
    over the x-axis).

    Args:
    - x0 (float): The x-coordinate of the center point.
    - y0 (float): The y-coordinate of the center point.
    - r0 (float): The radius of the first circle centered at A.
    - r1 (float): The radius of the second circle centered at B.
    - theta (float): The angle in radians between the x-axis and the line from the center point to point B.
    - n (int): The number of points to generate.

    Returns:
    - list of tuples: The list of n points (x, y) on the circle.
    """
    # Use the find_point function to get xs and distance
    xs, distance = find_point(x0, r0, r1, theta)

    # Angle at which point B is located
    xB = x0 + r1 * np.cos(theta)
    yB = y0 + r1 * np.sin(theta)

    # Calculate the angle between consecutive points
    delta_angle = 2 * theta / (n - 1)  # Equidistant angles

    points = []

    for i in range(n):
        # Angle for the current point
        angle = theta - i * delta_angle

        # Parametric equation of the circle
        x = xs + distance * np.cos(angle)
        y = y0 + distance * np.sin(angle)

        points.append([round(x), round(y)])

    return points

if __name__ == "__main__":
    # Example usage:
    x0, y0, r0, r1, theta = 0, 0, 100, 100, math.radians(45)  # Theta in radians
    n = 8  # Number of points to generate
    points = generate_points(x0, y0, r0, r1, theta, n)
    print(points)
