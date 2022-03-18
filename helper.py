# Austin Cubbage
# 3/11/15
# The Helper class. This class provides methods that help compute the
# mandelbrot set.

import math

MAX = 255

class Helper:

    # Pre: Takes the width and height of the canvas window,
    #      also takes the complex number range for both a and b.
    def __init__(self, canvas_width, canvas_height, complex_range_a,
                 complex_range_b):
        self.canvas_width, self.canvas_height = canvas_width, canvas_height
        self.complex_lower_a, self.complex_upper_a = complex_range_a
        self.complex_lower_b, self.complex_upper_b = complex_range_b

    # Pre:  Takes the canvas coordinates that you want converted, x and y.
    #       Also takes the width and height of the canvas.
    # Post: Returns the same location in complex coordinates.
    def convert_coords(self, x, y):
        complex_x = ((x / self.canvas_width) *
                     (self.complex_upper_a - self.complex_lower_a) +
                     self.complex_lower_a)
        complex_y = ((y / self.canvas_height) *
                     (self.complex_upper_b - self.complex_lower_b) +
                      self.complex_lower_b)
        return complex_x, complex_y

    # Pre:  Takes the complex number you want to compute the number
    #       of iterations for. Also takes the previous iteration of
    #       the algorithm, also a complex number.
    #       Also takes the current iteration that the method is at.
    # Post: Returns the number of iterations it took to reach an absolute
    #       value of 2.
    def compute_num_iterations(self, complex_number, previous, iteration):
        complex_n = (previous.multiply(previous)).add(complex_number)
        magnitude = math.fabs(complex_n.magnitude())

        if magnitude >= 2 or iteration >= MAX:
            iterations = iteration
        else:
            iterations = self.compute_num_iterations(complex_number,
            complex_n, iteration + 1)
        return iterations






























