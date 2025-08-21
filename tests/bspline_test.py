"""
In this file we will test to create B-Splines as defined by the B-Spline theory.
We will compare our implementation with the one provided by scipy.interpolate to see how they perform.

* scipy is insanely fast so lets use that but we learnt a lot by implementing it ourselves.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline, make_interp_spline


def basis_function_recursive(knots: np.ndarray, degree: int, t: float, i: int) -> float:
    """
    Recursive definition of the B-spline basis function.
    :param knots: The knot vector.
    :param degree: The degree of the B-spline.
    :param t: The parameter value at which to evaluate the basis function.
    :param i: The index of the basis function.
    """
    if degree == 0:
        if knots[i] <= t <= knots[i + 1]:
            return 1.0
        else:
            return 0.0
    
    coefficient1 = 0.0
    if knots[i + degree] != knots[i]:
        coefficient1 = (t - knots[i]) / (knots[i + degree] - knots[i])

    coefficient2 = 0.0
    if knots[i + degree + 1] != knots[i + 1]:
        coefficient2 = (knots[i + degree + 1] - t) / (knots[i + degree + 1] - knots[i + 1])
    
    return coefficient1 * basis_function_recursive(knots, degree - 1, t, i) + \
              coefficient2 * basis_function_recursive(knots, degree - 1, t, i + 1)
    
def b_spline(control_points: np.ndarray, degree: int = 3, knots: np.ndarray | None = None, num_points: int = 100) -> np.ndarray:
    """
    Compute the B-spline curve given control points and degree.
    :param control_points: The control points of the B-spline.
    :param degree: The degree of the B-spline.
    :param knots: The knot vector.
    :param num_points: Number of points to evaluate the B-spline.
    """
    
    # check if knots are correctly provided (non-decreasing and sequential)
    if knots is None:
        raise ValueError("Knot vector must be provided.")
    if len(knots) < degree + 1 + len(control_points):
        raise ValueError("Knot vector must have at least degree + 1 + number of control points elements.")
    if not all(knots[i] <= knots[i + 1] for i in range(len(knots) - 1)):
        raise ValueError("Knot vector must be non-decreasing.")
    
    # normalize knots in [0, 1]
    # knots = (knots - knots[0]) / (knots[-1] - knots[0])

    # generate linspace of t values to be evaluated
    t_values = np.linspace(knots[degree], knots[-degree-1], num_points)

    curve_points = np.zeros((num_points, control_points.shape[1]))

    for j in range(num_points):
        t = t_values[j]
        for i in range(len(control_points)):
            b_i = basis_function_recursive(knots, degree, t, i)
            curve_points[j] += b_i * control_points[i]
        
    return curve_points

def main():
    control_points = np.array([[0, 0], [1, 2], [2, 0], [3, 3]])
    degree = 3
    num_points = 10000
    
    # Knot vector for a cubic B-spline
    knots = np.array([0, 0, 0, 0, 1, 1, 1, 1])

    # Evaluate the B-spline using our implementation
    start_time = time.time()
    our_spline = b_spline(control_points, degree=degree, knots=knots, num_points=num_points)
    # print(f"Manual spline generated: {our_spline}")
    our_time = time.time() - start_time
    
    # Evaluate the B-spline using scipy's implementation
    start_time = time.time()
    spline = BSpline(t=knots, c=control_points, k=degree)
    scipy_spline = spline(np.linspace(knots[degree], knots[-degree - 1], num_points))
    # print(f"Scipy spline generated: {scipy_spline}")
    scipy_time = time.time() - start_time
    
    print(f"Our B-Spline Time: {our_time:.6f} seconds")
    print(f"Scipy B-Spline Time: {scipy_time:.6f} seconds")
    
    # Plot the results
    plt.plot(our_spline[:, 0], our_spline[:, 1], label='Our B-Spline', color='blue')
    plt.plot(scipy_spline[:, 0], scipy_spline[:, 1], label='Scipy B-Spline', color='orange', linestyle='--')
    plt.scatter(control_points[:, 0], control_points[:, 1], color='red', label='Control Points')
    
    plt.title('B-Spline Comparison')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
   