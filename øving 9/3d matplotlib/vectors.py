
import numpy as np

class Vector:
    def __init__(self, axis):
        self.vec = np.array(axis)


    def __repr__(self):
        return f"Vector({self[0]}, {self[1]}, {self[2]})"

    def __str__(self):
        return f"{self[0]}i + {self[1]}j + {self[2]}k"

    def __getitem__(self, item):
        return self.vec[item]

    def __add__(self, other):
        return Vector(np.add(self.vec, other.vec))

    def __sub__(self, other):
        return Vector(np.subtract(self.vec, other.vec))

    def __mul__(self, other):
        if isinstance(other, Vector):  # Vector dot product
            return np.inner(self.vec, other.vec)

        elif isinstance(other, (int, float)):  # Scalar multiplication
            # print(self.vec, other, np.multiply(self.vec, other))
            return  Vector(np.multiply(self.vec, other))

        else:
            raise TypeError("operand must be Vector, int, or float")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(np.true_divide(self.vec, other))

        else:
            raise TypeError("operand must be int or float")

    def get_magnitude(self):
        return np.sqrt(self.vec.dot(self.vec)) # litt smart bruk av skalar produktet

    def normalize(self):
        magnitude = self.get_magnitude()
        # print(Vector(self.vec / magnitude))
        return Vector(self.vec / magnitude)
