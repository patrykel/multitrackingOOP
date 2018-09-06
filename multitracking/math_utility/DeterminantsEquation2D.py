

class DeterminantsEquation2D():
    '''
    | a1 b1 | * | x | = | c1 |
    | a2 b2 |   | y |   | c2 |

  	W  = | a1 b1 | = a1 * b2 - b1 * a2
         | a2 b2 |

    Wx = | c1 b1 | = c1 * b2 - b1 * c2
         | c2 b2 |

    Wy = | a1 c1 | = a1 * c2 - c1 * a2
         | a2 c2 |
    '''

    def __init__(self, a1, b1, c1, a2, b2, c2):
        self.a1 = a1
        self.b1 = b1
        self.c1 = c1

        self.a2 = a2
        self.b2 = b2
        self.c2 = c2


    def compute_solution(self):
        w   = self.count_w()
        w_x = self.count_wx()
        w_y = self.count_wy()

        x = w_x / w
        y = w_y / w

        return x, y

    def count_w(self):
        return self.a1 * self.b2 - self.b1 * self.a2

    def count_wx(self):
        return self.c1 * self.b2 - self.b1 * self.c2

    def count_wy(self):
        return self.a1 * self.c2 - self.c1 * self.a2
