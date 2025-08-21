import numpy as np
import matplotlib.pyplot as plt


def main():
    y_array = np.array([157.7485, 157.5737, 157.411, 157.2605, 157.1221, 156.9959, 156.8818, 156.7799, 156.69, 156.6124])

    plt.plot(y_array, label="Y Values")
    plt.grid()
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()