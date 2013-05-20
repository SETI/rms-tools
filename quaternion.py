################################################################################
# quaternion.py
#
# A class and methods to manipulate quaternions and to convert between
# quaternions and rotation matrices.
#
# Mark R. Showalter, SETI Institute, May 2013
################################################################################

import numpy as np

class Quaternion(object):
    """A class and methods to manipulate quaternions and to convert between
    quaternions and rotation matrices.
    """

    EPSILON = 1.e-320

    def __init__(self, values, vector=None):
        """Constructor for a quaternion.

        Input:
            values      one or more 4-vectors defining the components of a
                        quaternion. Alternatively, the scalar parts if the
                        second argument is provided.
            vector      if not None, the vector components of the quaternions.
        """

        if vector is None:
            self.values = np.asfarray(values)
        else:
            scalar = np.asarray(values)
            vector = np.asarray(vector)
            assert vector.shape[:-1] == scalar.shape
            assert vector.shape[-1] == 3

            self.values = np.empty(scalar.shape + (4,))
            self.values[..., 0]   = scalar
            self.values[..., 1:4] = vector

        assert self.values.shape[-1] == 4
        self.scalar = self.values[..., 0]
        self.vector = self.values[..., 1:4]

        self.shape = self.scalar.shape

    def reshape(self, shape):
        shape = tuple(shape) + (4,)
        return Quaternion(self.values.reshape(shape))

    def __mul__(self, b):
        if type(b) == Quaternion:

            # Make the lengths of the shapes equal
            a = self
            diff = len(a.shape) - len(b.shape)
            if diff < 0:
                a = a.reshape(diff * [1] + list(a.shape))
            if diff > 0:
                b = b.reshape(diff * [1] + list(b.shape))

            # Define the broadcasted shape
            shape = tuple(np.maximum(a.shape, b.shape)) + (4,)
            values = np.empty(shape)

            # Construct the new array
            values[...,0] = (a.scalar * b.scalar -
                             np.sum(a.vector * b.vector, axis=-1))
            values[...,1:4] = (a.scalar[..., np.newaxis] * b.vector +
                               b.scalar[..., np.newaxis] * a.vector +
                               np.cross(a.vector, b.vector))

            # Return the quaternion
            return Quaternion(values)

        if np.shape(b) != ():
            b = np.array(b)[..., np.newaxis]

        return Quaternion(b * self.values)

    def __rmul__(self, a):
        if np.shape(a) != ():
            a = np.array(a)[..., np.newaxis]
        return Quaternion(a * self.values)

    def __invert__(self):
        """Inverse of quaternion."""
        values = self.values.copy()
        values[...,3] *= -1.
        return Quaternion(values)

    def __div__(self, b):
        if type(b) == Quaternion:
            return self * b.__invert__()

        if np.shape(b) != ():
            b = np.array(b)[..., np.newaxis]

        return Quaternion(self.values / b)

    def __rdiv__(self, b):
        return b * self.__invert__()

    def __add__(self, b):
        assert type(b) == Quaternion
        return Quaternion(self.values + b.values)

    def __sub__(self, b):
        assert type(b) == Quaternion
        return Quaternion(self.values - b.values)

    def __abs__(self):
        return np.sqrt(np.sum(self.values**2, axis=-1))

    def normalize(self):
        return Quaternion(self.values / abs(self))

    def to_matrix(self):

        result = np.empty(self.shape + (3,3))

        normalized = self.normalize()
        s  = normalized.scalar
        vx = normalized.vector[...,0]
        vy = normalized.vector[...,1]
        vz = normalized.vector[...,2]

        result[...,0,0] = 1. - 2.*(vy**2 + vz**2)
        result[...,0,1] =      2.*(vx*vy - s*vz)
        result[...,0,2] =      2.*(vx*vz + s*vy)
        result[...,1,0] =      2.*(vx*vy + s*vz)
        result[...,1,1] = 1. - 2.*(vx**2 + vz**2)
        result[...,1,2] =      2.*(vy*vz - s*vx)
        result[...,2,0] =      2.*(vx*vz - s*vy)
        result[...,2,1] =      2.*(vy*vz + s*vx)
        result[...,2,2] = 1. - 2.*(vx**2 + vy**2)

        return result

    @staticmethod
    def from_matrix(m):

        m = np.asfarray(m)[np.newaxis]
        values = np.empty(m.shape[:-2] + (4,))

        s = m[...,0,0] + m[...,1,1] + m[...,2,2] + 1.
        s = np.sqrt(np.maximum(s, Quaternion.EPSILON))
        values[...,0] = 0.5 * s
        s = 0.5 / s
        values[...,1] = (m[...,2,1] - m[...,1,2]) * s
        values[...,2] = (m[...,0,2] - m[...,2,0]) * s
        values[...,3] = (m[...,1,0] - m[...,0,1]) * s

        mask = (m[...,0,0] >= np.maximum(m[...,1,1], m[...,2,2]))
        if np.any(mask):
            s = m[...,0,0] - m[...,1,1] - m[...,2,2] + 1.
            mask = mask & (s > 0.)
            s = np.sqrt(np.maximum(s, Quaternion.EPSILON))
            values[...,1][mask] = (0.5 * s)[mask]
            s = 0.5 / s
            values[...,2][mask] = ((m[...,0,1] + m[...,1,0]) * s)[mask]
            values[...,3][mask] = ((m[...,2,0] + m[...,0,2]) * s)[mask]
            values[...,0][mask] = ((m[...,2,1] - m[...,1,2]) * s)[mask]

        mask = (m[...,1,1] >= np.maximum(m[...,0,0], m[...,2,2]))
        if np.any(mask):
            s = m[...,1,1] - m[...,2,2] - m[...,0,0] + 1.
            mask = mask & (s > 0.)
            s = np.sqrt(np.maximum(s, Quaternion.EPSILON))
            values[...,2][mask] = (0.5 * s)[mask]
            s = 0.5 / s
            values[...,3][mask] = ((m[...,1,2] + m[...,2,1]) * s)[mask]
            values[...,1][mask] = ((m[...,0,1] + m[...,1,0]) * s)[mask]
            values[...,0][mask] = ((m[...,0,2] - m[...,2,1]) * s)[mask]

        mask = (m[...,2,2] >= np.maximum(m[...,0,0], m[...,1,1]))
        if np.any(mask):
            s = m[...,2,2] - m[...,0,0] - m[...,1,1] + 1.
            mask = mask & (s > 0.)
            s = np.sqrt(np.maximum(s, Quaternion.EPSILON))
            values[...,3][mask] = (0.5 * s)[mask]
            s = 0.5 / s
            values[...,1][mask] = ((m[...,2,0] + m[...,0,2]) * s)[mask]
            values[...,2][mask] = ((m[...,1,2] + m[...,2,1]) * s)[mask]
            values[...,0][mask] = ((m[...,1,0] - m[...,0,1]) * s)[mask]

        return Quaternion(values[0])

    def __str__(self):
        return 'Quaternion(' + str(self.values) + ')'

    def __repr__(self):
        return 'Quaternion' + repr(self.values)[5:]

