from geometry_classes.Vector2D import *


class GeometryInclusionTest:

    # by: https://stackoverflow.com/questions/2752725/finding-whether-a-point-lies-inside-a-rectangle-or-not/2763387#2763387
    @staticmethod
    def inside_rect(rect_points, P):
        '''
        rect_points - consequtive points of rectangle - can be clockwise and counter clockwise
        P           - tested point (Point2D class)

         A ___________D
          |          |
          |          |
          |__________|
         B           C

        (0 < AP ⋅ AB < AB ⋅ AB) and (0 < AP ⋅ AD < AD ⋅ AD)
        '''
        A, B, C, D = rect_points

        AB = Vector2D(start=A, end=B)
        AD = Vector2D(start=A, end=D)
        AP = Vector2D(start=A, end=P)

        return 0.0 < AB.dot(AP) and \
               AB.dot(AP) < AB.dot(AB) and \
               0.0 < AD.dot(AP) and \
               AD.dot(AP) < AD.dot(AD)

    # by: https://www.gamedev.net/forums/topic/295943-is-this-a-better-point-in-triangle-test-2d/?tab=comments#comment-2873873
    @staticmethod
    def inside_triangle(triangle_points, P):
        '''
        triangle_points - consequtive points of triangle - can be clockwise and counter clockwise
        P               - tested point (Point2D class)
        '''
        A, B, C = triangle_points

        b0 = Vector2D(P.x - A.x, P.y - A.y).dot(Vector2D(A.y - B.y, B.x - A.x)) > 0.0
        b1 = Vector2D(P.x - B.x, P.y - B.y).dot(Vector2D(B.y - C.y, C.x - B.x)) > 0.0
        b2 = Vector2D(P.x - C.x, P.y - C.y).dot(Vector2D(C.y - A.y, A.x - C.x)) > 0.0

        return b0 == b1 and b1 == b2