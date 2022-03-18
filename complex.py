# Austin Cubbage
# 3/11/15
# The complex numbers class! This class is used to do computations
# with complex numbers for the mandelbrot renderings.

class Complex:

    # Pre: Takes the complex numbers a and b values
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.c = complex(a, b)

    # Pre: Takes the other complex number object
    # Post: Returns a new complex number, the sum of the two numbers
    def add(self, additive):
        new_a = self.a + additive.a
        new_b = self.b + additive.b
        return Complex(new_a, new_b)

    # Pre:  Takes the other complex number object
    # Post: Returns a new complex number, the product of the two numbers
    def multiply(self, multiplier):
        real1, imag1 = self.a, self.b
        real2, imag2 = multiplier.a, multiplier.b
        new_a = real1 * real2 - imag1 * imag2
        new_b = real1 * imag2 + real2 * imag1
        return Complex(new_a, new_b)

    # Pre:  None
    # Post: Returns the distance from the origin that the complex number is.
    def magnitude(self):
        value = ((self.a ** 2) + (self.b ** 2)) ** (1 / 2)
        return value

