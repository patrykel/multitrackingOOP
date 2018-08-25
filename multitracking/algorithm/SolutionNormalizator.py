from multitracking.algorithm.HitLinesProviderConfig import *

import numpy as np

class SolutionNormalizator:

    @staticmethod
    def normalize(solution):
        SolutionNormalizator.normalize_solution_vector(solution)
        SolutionNormalizator.normalize_solution_point(solution)


    @staticmethod
    def normalize_solution_vector(solution):
        dx, dy, dz = solution.x[-3:]

        vector_norm = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        dx = dx / vector_norm
        dy = dy / vector_norm
        dz = dz / vector_norm

        solution.x[-3:] = [dx, dy, dz]


    @staticmethod
    def normalize_solution_point(solution):
        if HitLinesProviderConfig.TRANSLATE_LINES:
            # At first we translated all hit_lines.
            # In the way that first silicon detector was in z = 0
            # Then we applied ADDITIONAL TRANSLATION
            # So that now track initial point is in z = 0, but, first det_z = +/- ADDITIONAL TRANSLATION

            x, y, dx, dy, dz = solution.x

            additional_translation = HitLinesProviderConfig.ADDITIONAL_TRANSLATION \
                                     * np.sign(HitLinesProviderConfig.LOWEST_ABS_SILICON_Z)

            k_z = additional_translation / dz

            new_x = x + k_z * dx    # new_x - x coordinate of track on z = LOWEST_SILICON_Z
            new_y = y + k_z * dy    # new_y - y coordinate of track on z = LOWEST_SILICON_Z

            solution.x[:2] = [new_x, new_y]