import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    
    def distance_to_origin(self):
        return math.hypot(self.x, self.y)
    
    def distance_to_other(self, other : "Point"):
        return math.hypot(self.x - other.x, self.y - other.y)


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_exist(self):
        a, b, c = self.a, self.b, self.c
        return (
            a + b > c and
            a + c > b and
            b + c > a
        )

    def triangle_type(self):
        if not self.is_exist():
            return None

        a, b, c = self.a, self.b, self.c
        sides = sorted([a, b, c])

        if a == b == c:
            return "Tam giác đều"
        if a == b or b == c or a == c:
            return "Tam giác cân"
        if sides[0]**2 + sides[1]**2 == sides[2]**2:
            return "Tam giác vuông"
        if sides[0]**2 + sides[1]**2 < sides[2]**2:
            return "Tam giác tù"
        return "Tam giác nhọn"

    def perimeter(self):
        return self.a + self.b + self.c if self.is_exist() else None

    def area(self):
        if not self.is_exist():
            return None
        p = self.perimeter() / 2
        return math.sqrt(p * (p-self.a) * (p-self.b) * (p-self.c))

    def incircle_radius(self):
        if not self.is_exist():
            return None
        return 2 * self.area() / self.perimeter()

    def circumcircle_radius(self):
        if not self.is_exist():
            return None
        return self.a * self.b * self.c / (4 * self.area())
