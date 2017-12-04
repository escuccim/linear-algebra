from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 6


class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def add(self, vector):
        result = []
        try:
            if (vector.dimension) != self.dimension:
                raise ValueError

            for i in range(0, self.dimension):
                result.append(self.coordinates[i] + vector.coordinates[i])

            resultVector = Vector(result)
            return resultVector

        except ValueError:
            raise ValueError("The vectors are of different sizes!")

        except TypeError:
            raise TypeError('The vector must be added to another vector')

    def subtract(self, vector):
        result = []

        try:
            if (vector.dimension) != self.dimension:
                raise ValueError

            for i in range(0, self.dimension):
                result.append(self.coordinates[i] - vector.coordinates[i])

            resultVector = Vector(result)
            return resultVector

        except ValueError:
            raise ValueError("The vectors are of different sizes!")

        except TypeError:
            raise TypeError('The vector must be added to another vector')

    def scale(self, num):
        result = [Decimal(num) * x for x in self.coordinates]

        return Vector(result)

    def magnitude(self):
        squared = [x ** 2 for x in self.coordinates]
        return Decimal(sqrt(sum(squared)))

    def normalize(self):
        try:
            magnitude = self.magnitude()
            if magnitude is not 0:
                return self.scale(Decimal(1.0) / magnitude)
            else:
                return self

        except ZeroDivisionError:
            raise Exception("Cannot normalize zero vector!")

    def dotproduct(self, vector):
        result = 0
        return sum([x * y for x, y in zip(self.coordinates, vector.coordinates)])

    def angle(self, vector, in_degrees=False):
        try:
            if self == vector:
                return 0
            u1 = self.normalize()
            u2 = vector.normalize()
            angle_in_radians = acos(u1.dotproduct(u2))

            if in_degrees:
                return angle_in_radians * (180.0 / pi)
            else:
                return angle_in_radians

        except Exception  as e:
            raise e

    def is_orthogonal(self, vector, tolerance=1e-10):
        return abs(self.dotproduct(vector)) < tolerance

    def is_zero(self, tolerance=1e-10):
        return self.magnitude < tolerance

    def is_parallel(self, vector):
        return self.is_zero() or vector.is_zero() or self.angle(vector) == 0 or self.angle(vector) == pi

    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            weight = self.dotproduct(u)
            return u.scale(weight)
        except Exception as e:
            raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.subtract(projection)

        except Exception as e:
            raise e

    def cross(self, vector):
        try:
            if self.dimension != 3 or vector.dimension != 3:
                raise ValueError

            result = [(self.coordinates[1] * vector.coordinates[2]) - (vector.coordinates[1] * self.coordinates[2]),
                      -((self.coordinates[0] * vector.coordinates[2]) - (vector.coordinates[0] * self.coordinates[2])),
                      (self.coordinates[0] * vector.coordinates[1]) - (vector.coordinates[0] * self.coordinates[1])]
            return Vector(result)

        except ValueError:
            raise Exception("Vectors must be three dimensional!")

    def parallelogram_with_area(self, vector):
        cross = self.cross(vector)
        return cross.magnitude()

    def triangle_with_area(self, vector):
        return self.parallelogram_with_area(self, vector) / Decimal(2.0)