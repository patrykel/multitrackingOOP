class Point2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "x = {}\ty = {}".format(self.x, self.y)

    def move(self, vector):
        self.x += vector.x
        self.y += vector.y

    def rotate_around_point(self, other, direction):
        s = direction.dy
        c = direction.dx

        new_x = c * (self.x - other.x) - s * (self.y - other.y) + other.x
        new_y = s * (self.x - other.x) + c * (self.y - other.y) + other.y

        self.x = new_x
        self.y = new_y