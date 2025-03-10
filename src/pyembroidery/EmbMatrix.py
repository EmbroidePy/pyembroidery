import math


class EmbMatrix:
    def __init__(self, m=None):
        if m is None:
            self.m = self.get_identity()
        else:
            self.m = m

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return self.m == other.m

    def __matmul__(self, other):
        return EmbMatrix(EmbMatrix.matrix_multiply(self.m, other.m))

    def __rmatmul__(self, other):
        return EmbMatrix(EmbMatrix.matrix_multiply(self.m, other.m))

    def __imatmul__(self, other):
        self.m = EmbMatrix.matrix_multiply(self.m, other.m)

    def __str__(self):
        return "[%3f, %3f, %3f\n %3f, %3f, %3f\n %3f, %3f, %3f]" % self.m

    def get_matrix(self):
        return self.m

    def reset(self):
        self.m = self.get_identity()

    def inverse(self):
        m = self.m
        m48s75 = m[4] * m[8] - m[7] * m[5]
        m38s56 = m[5] * m[6] - m[3] * m[8]
        m37s46 = m[3] * m[7] - m[4] * m[6]
        det = m[0] * m48s75 + m[1] * m38s56 + m[2] * m37s46
        inverse_det = 1.0 / float(det)
        self.m = [
            m48s75 * inverse_det,
            (m[2] * m[7] - m[1] * m[8]) * inverse_det,
            (m[1] * m[5] - m[2] * m[4]) * inverse_det,
            m38s56 * inverse_det,
            (m[0] * m[8] - m[2] * m[6]) * inverse_det,
            (m[3] * m[2] - m[0] * m[5]) * inverse_det,
            m37s46 * inverse_det,
            (m[6] * m[1] - m[0] * m[7]) * inverse_det,
            (m[0] * m[4] - m[3] * m[1]) * inverse_det,
        ]

    def post_scale(self, sx=1, sy=None, x=0, y=0):
        if sy is None:
            sy = sx
        if x is None:
            x = 0
        if y is None:
            y = 0
        if x == 0 and y == 0:
            self.m = self.matrix_multiply(self.m, self.get_scale(sx, sy))
        else:
            self.post_translate(x, y)
            self.post_scale(sx, sy)
            self.post_translate(-x, -y)

    def post_translate(self, tx, ty):
        self.m = self.matrix_multiply(self.m, self.get_translate(tx, ty))

    def post_rotate(self, theta, x=0, y=0):
        if x is None:
            x = 0
        if y is None:
            y = 0
        if x == 0 and y == 0:
            self.m = self.matrix_multiply(self.m, self.get_rotate(theta))
        else:
            self.post_translate(x, y)
            self.post_rotate(theta)
            self.post_translate(-x, -y)

    def post_cat(self, matrix_list):
        for mx in matrix_list:
            self.m = self.matrix_multiply(self.m, mx)

    def pre_scale(self, sx=1, sy=None):
        if sy is None:
            sy = sx
        self.m = self.matrix_multiply(self.get_scale(sx, sy), self.m)

    def pre_translate(self, tx, ty):
        self.m = self.matrix_multiply(self.get_translate(tx, ty), self.m)

    def pre_rotate(self, theta):
        self.m = self.matrix_multiply(self.get_rotate(theta), self.m)

    def pre_cat(self, matrix_list):
        for mx in matrix_list:
            self.m = self.matrix_multiply(mx, self.m)

    def point_in_matrix_space(self, v0, v1=None):
        m = self.m
        if v1 is None:
            try:
                return [
                    v0[0] * m[0] + v0[1] * m[3] + 1 * m[6],
                    v0[0] * m[1] + v0[1] * m[4] + 1 * m[7],
                    v0[2],
                ]
            except IndexError:
                return [
                    v0[0] * m[0] + v0[1] * m[3] + 1 * m[6],
                    v0[0] * m[1] + v0[1] * m[4] + 1 * m[7]
                    # Must not have had a 3rd element.
                ]
        return [v0 * m[0] + v1 * m[3] + 1 * m[6], v0 * m[1] + v1 * m[4] + 1 * m[7]]

    def apply(self, v):
        m = self.m
        nx = v[0] * m[0] + v[1] * m[3] + 1 * m[6]
        ny = v[0] * m[1] + v[1] * m[4] + 1 * m[7]
        v[0] = nx
        v[1] = ny

    @staticmethod
    def get_identity():
        return 1, 0, 0, 0, 1, 0, 0, 0, 1  # identity

    @staticmethod
    def get_scale(sx, sy=None):
        if sy is None:
            sy = sx
        return sx, 0, 0, 0, sy, 0, 0, 0, 1

    @staticmethod
    def get_translate(tx, ty):
        return 1, 0, 0, 0, 1, 0, tx, ty, 1

    @staticmethod
    def get_rotate(theta):
        tau = math.pi * 2
        theta *= tau / 360
        ct = math.cos(theta)
        st = math.sin(theta)
        return ct, st, 0, -st, ct, 0, 0, 0, 1

    @staticmethod
    def matrix_multiply(m0, m1):
        return [
            m1[0] * m0[0] + m1[1] * m0[3] + m1[2] * m0[6],
            m1[0] * m0[1] + m1[1] * m0[4] + m1[2] * m0[7],
            m1[0] * m0[2] + m1[1] * m0[5] + m1[2] * m0[8],
            m1[3] * m0[0] + m1[4] * m0[3] + m1[5] * m0[6],
            m1[3] * m0[1] + m1[4] * m0[4] + m1[5] * m0[7],
            m1[3] * m0[2] + m1[4] * m0[5] + m1[5] * m0[8],
            m1[6] * m0[0] + m1[7] * m0[3] + m1[8] * m0[6],
            m1[6] * m0[1] + m1[7] * m0[4] + m1[8] * m0[7],
            m1[6] * m0[2] + m1[7] * m0[5] + m1[8] * m0[8],
        ]
