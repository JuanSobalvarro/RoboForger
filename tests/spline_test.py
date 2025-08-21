"""
In this file we will test functions to see how splines works and how can we approximate a use of them to be used in the RoboForger main library.

We use scipy.interpolate to create functioning splines then create our own solution to see which one is better. Obviosly we prefer to use our own solution
so we can have less dependencies and more control over the code. So lets check which one is better.

Using numpy for the math representation and matplotlib for the visualization of the results.
"""
import time

import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import CubicSpline


def pol_solution(control_points: np.ndarray, degree: int = 3) -> np.ndarray:
    """
    This function will return the coefficients of the polynomial that represents the function that passes through the control points.
    Given the control points and the degree of the polynomial, we will solve for the Ax=B system where x vector is the coefficients of the polynomial, A are the t values raised to the power of the degree and B are the control points values.
    We take t values in the range of 0 to 1, so if we have n control points, we will have n t values that are evenly spaced in the range of 0 to 1.
    Also we start with the t with exponent 0 and go up to the degree of the polynomial, so we will have degree + 1 columns in the A matrix.
    The return coefficients are in order from the highest degree to the lowest degree. Ex eq ^ 3: a*t^3 + b*t^2 + c*t + d
    :param control_points: The control points of the spline.
    :param degree: The degree of the polynomial.
    """

    A = np.zeros(shape=(len(control_points), degree + 1))
    B = control_points
    t = np.linspace(0, 1, len(control_points)) # linspace creates a range [0, 1] *inclusive
    
    # populate the A matrix that can look like this for degree 3:
    # [t1^0 == 1, t1^1, t1^2, t1^3]
    # [1, t2^1, t2^2, t2^3]
    # [1, t3^1, t3^2, t3^3]
    for i in range(len(control_points)):
        for j in range(degree + 1):
            A[i, j] = t[i] ** j
    
    # Solve the system Ax = B for x, where x are the coefficients of the polynomial
    coeffs = np.linalg.solve(A, B)
    
    return coeffs[::-1]  # reverse the order of the coefficients

def pol_eval(coeffs: np.ndarray, t: float) -> float:
    """
    Evaluate the polynomial at a given t value using the coefficients.
    :param coeffs: The coefficients of the polynomial.
    :param t: The t value to evaluate the polynomial at.
    """
    degree = len(coeffs) - 1
    result = 0.0
    for i in range(degree + 1):
        result += coeffs[i] * (t ** (degree - i))
    return result

def pol_spline(control_points: np.ndarray, degree: int = 3, num_points: int = 100) -> np.ndarray:
    coeffs = pol_solution(control_points, degree)
    t_values = np.linspace(0, 1, num_points)
    return np.array([pol_eval(coeffs, t) for t in t_values])

def main():

    scipy_time = 0.0
    our_time = 0.0

    # Example control points
    control_points = np.array([7.89575456, 10.00933683, 11.18132927, 12.85656739])
    
    # take scipy time
    start_time = time.time()
    # Create a cubic spline using scipy
    cs = CubicSpline(np.linspace(0, 1, len(control_points)), control_points)
    
    # Evaluate the spline at 100 points
    t_values = np.linspace(0, 1, 100)
    scipy_spline = cs(t_values)
    scipy_time = time.time() - start_time
    
    # Evaluate our polynomial spline
    start_time = time.time()
    our_spline = pol_spline(control_points, degree=3, num_points=100)
    our_time = time.time() - start_time

    print(f"Scipy Cubic Spline Time: {scipy_time:.6f} seconds")
    print(f"Our Polynomial Spline Time: {our_time:.6f} seconds")

    # Plot the results
    plt.plot(t_values, scipy_spline, label='Scipy Cubic Spline', color='blue')
    plt.plot(t_values, our_spline, label='Our Polynomial Spline', color='orange', linestyle='--')
    plt.scatter(np.linspace(0, 1, len(control_points)), control_points, color='red', label='Control Points')
    
    plt.title('Comparison of Scipy Cubic Spline and Our Polynomial Spline')
    plt.xlabel('t')
    plt.ylabel('Spline Value')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()