class Vector2D:
    def __init__(self, x=0.0, y=0.0, start=None, end=None):
        if start is None or end is None:
            self.x = x
            self.y = y
        else:
            self.x = end.x - start.x
            self.y = end.y - start.y

    def __repr__(self):
        return "x = {}\ty = {}".format(self.x, self.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y