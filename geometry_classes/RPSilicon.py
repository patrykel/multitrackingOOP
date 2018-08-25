from geometry_classes.GeometryInclusionTest import *
from geometry_classes.Direction2D import *
from geometry_classes.Point2D import *
from geometry_classes.Vector2D import *

import copy
import numpy as np

'''
OVERVIEW:

 L(x,y)---------T(x,y)              Top             a = 36.07  [mm] (side length)
 |              |                   /\              e = 22.276 [mm] (edge length)
 |              |                 a/  \ b
 |              |                 /    \
 |       + (0,0)|            Left/      \Right      T_x,  T_y  =  a/2.0,                 a/2.0
 EL(x,y)        |                \      /           L_x,  L_y  = -a/2.0,                 a/2.0
  \             |                c\    /d           R_x,  R_y  =  a/2.0,                -a/2.0
   \            |                  ====             EL_x, EL_y = -a/2.0,                -a/2.0 + e/np.sqrt(2)
    \ER(x,y)----R(x,y)             edge (e)         ER_x, ER_y = -a/2.0 + e/np.sqrt(2), -a/2.0
'''

class RPSilicon:
    A = 36.07  # side length [mm]
    E = 22.276  # edge length [mm]

    d_T = Point2D(A / 2.0, A / 2.0)  # T
    d_L = Point2D(-A / 2.0, A / 2.0)  # L
    d_R = Point2D(A / 2.0, -A / 2.0)  # R
    d_EL = Point2D(-A / 2.0, -A / 2.0 + E / np.sqrt(2))  # EL
    d_ER = Point2D(-A / 2.0 + E / np.sqrt(2), -A / 2.0)  # ER

    def __init__(self, center, direction, siId, T=d_T, L=d_L, R=d_R, EL=d_EL, ER=d_ER):
        self.center = center
        self.direction = direction
        self.siId = siId

        self.T = copy.deepcopy(T)
        self.L = copy.deepcopy(L)
        self.R = copy.deepcopy(R)
        self.EL = copy.deepcopy(EL)
        self.ER = copy.deepcopy(ER)
        self.points = [self.R, self.T, self.L, self.EL, self.ER]  # In sequence

        # MOVE DETECTOR POINTS
        self.move(Vector2D(self.center.x, self.center.y), self.points)  # general position

        # ROTATE AROUND CENTER
        rot_direction = self.get_rot_direction()
        self.rotate_around_center(self.points, rot_direction)

    def __repr__(self):
        return "T = {} \nL = {} \nR = {} \nEL = {}\nER = {}".format(self.T, self.L, self.R, self.EL, self.ER)

    def move(self, vector, points):
        for p in points:
            p.move(vector)

    def rotate_around_center(self, points, direction):
        for p in points:
            p.rotate_around_point(self.center, direction)

    def get_rot_direction(self):
        arm = int(self.siId / 1000)
        if arm == 0 and self.siId % 2 == 0:
            return self.direction
        elif arm == 0 and self.siId % 2 == 1:
            return Direction2D(self.direction.dy, -self.direction.dx)
        elif arm == 1 and self.siId % 2 == 0:
            return Direction2D(self.direction.dy, -self.direction.dx)
        else:
            return self.direction

    def contains(self, P):
        ''' check if detector plane contains point P'''
        det_square_points = self.get_det_square_points()
        det_missing_triangle_points = self.get_missing_triangle_points()

        return GeometryInclusionTest.inside_rect(det_square_points, P) \
               and not GeometryInclusionTest.inside_triangle(det_missing_triangle_points, P)

    def get_det_square_points(self):
        TL = Vector2D(start=self.T, end=self.L)
        r_B = copy.deepcopy(self.R)  # BOTTOM point
        r_B.move(TL)

        r_T = copy.deepcopy(self.T)
        r_L = copy.deepcopy(self.L)
        r_R = copy.deepcopy(self.R)

        return np.array([r_T, r_L, r_B, r_R])  # TOP, LEFT, BOTTOM, RIGHT

    def get_missing_triangle_points(self):
        TL = Vector2D(start=self.T, end=self.L)
        r_B = copy.deepcopy(self.R)  # BOTTOM point
        r_B.move(TL)

        r_EL = copy.deepcopy(self.EL)
        r_ER = copy.deepcopy(self.ER)

        return np.array([r_B, r_EL, r_ER])