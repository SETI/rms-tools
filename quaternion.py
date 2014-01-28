################################################################################
# quaternion.py
#
# A class and methods to manipulate quaternions and to convert between
# quaternions and rotation matrices.
#
# Mark R. Showalter, SETI Institute, May 2013
# 6/13 MRS: Fixed one bug in from_matrix, added Euler angle support.
################################################################################

import numpy as np

class Quaternion(object):
    """A class and methods to manipulate quaternions and to convert between
    quaternions and rotation matrices.
    """

    EPSILON = np.finfo(float).eps * 4.0
    TWOPI = 2. * np.pi

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
        values[...,1:4] *= -1.
        values /= np.sum(values**2, axis=-1)[..., np.newaxis]
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
        return Quaternion(self.values / abs(self)[..., np.newaxis])

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
            values[...,0][mask] = ((m[...,0,2] - m[...,2,0]) * s)[mask]

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

################################################################################
# Decomposition into rotations
#
# From: http://www.lfd.uci.edu/~gohlke/code/transformations.py.html
#
# A triple of Euler angles can be applied/interpreted in 24 ways, which can
# be specified using a 4 character string or encoded 4-tuple:
# 
#   *Axes 4-string*: e.g. 'sxyz' or 'ryxy'
# 
#   - first character : rotations are applied to 's'tatic or 'r'otating frame
#   - remaining characters : successive rotation axis 'x', 'y', or 'z'
# 
#   *Axes 4-tuple*: e.g. (0, 0, 0, 0) or (1, 1, 1, 1)
# 
#   - inner axis: code of axis ('x':0, 'y':1, 'z':2) of rightmost matrix.
#   - parity : even (0) if inner axis 'x' is followed by 'y', 'y' is followed
#     by 'z', or 'z' is followed by 'x'. Otherwise odd (1).
#   - repetition : first and last axis are same (1) or different (0).
#   - frame : rotations are applied to static (0) or rotating (1) frame.
################################################################################

    # axis sequences for Euler angles
    _NEXT_AXIS = [1, 2, 0, 1]

    # map axes strings to/from tuples of inner axis, parity, repetition, frame
    _AXES2TUPLE = {
        'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
        'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
        'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
        'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
        'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
        'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
        'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
        'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}

    _TUPLE2AXES = dict((v, k) for k, v in _AXES2TUPLE.items())

    @staticmethod
    def euler_to_matrix(ai, aj, ak, axes='rzxz'):
        """Return homogeneous rotation matrix from Euler angles and axis
        sequence.

        ai, aj, ak : Euler's roll, pitch and yaw angles
        axes : One of 24 axis sequences as string or encoded tuple

        >>> R = euler_matrix(1, 2, 3, 'syxz')
        >>> np.allclose(np.sum(R[0]), -1.34786452)
        True
        >>> R = euler_matrix(1, 2, 3, (0, 1, 0, 1))
        >>> np.allclose(np.sum(R[0]), -0.383436184)
        True
        >>> ai, aj, ak = (4*np.pi) * (np.random.random(3) - 0.5)
        >>> for axes in _AXES2TUPLE.keys():
        ...    R = euler_matrix(ai, aj, ak, axes)
        >>> for axes in _TUPLE2AXES.keys():
        ...    R = euler_matrix(ai, aj, ak, axes)

        """

        shape = np.shape(ai)
        assert np.shape(aj) == shape
        assert np.shape(ak) == shape

        try:
            (firstaxis, parity, repetition,
                                frame) = Quaternion._AXES2TUPLE[axes]
        except (AttributeError, KeyError):
            Quaternion._TUPLE2AXES[axes]  # validation
            firstaxis, parity, repetition, frame = axes

        i = firstaxis
        j = Quaternion._NEXT_AXIS[i+parity]
        k = Quaternion._NEXT_AXIS[i-parity+1]

        if frame:
            ai, ak = ak, ai

        if parity:
            ai, aj, ak = -ai, -aj, -ak

        si, sj, sk = np.sin(ai), np.sin(aj), np.sin(ak)
        ci, cj, ck = np.cos(ai), np.cos(aj), np.cos(ak)
        cc, cs = ci*ck, ci*sk
        sc, ss = si*ck, si*sk

        matrix = np.empty(shape + (3,3))
        if repetition:
            matrix[...,i,i] =  cj
            matrix[...,i,j] =  sj * si
            matrix[...,i,k] =  sj * ci
            matrix[...,j,i] =  sj * sk
            matrix[...,j,j] = -cj * ss + cc
            matrix[...,j,k] = -cj * cs - sc
            matrix[...,k,i] = -sj * ck
            matrix[...,k,j] =  cj * sc + cs
            matrix[...,k,k] =  cj * cc - ss
        else:
            matrix[...,i,i] =  cj * ck
            matrix[...,i,j] =  sj * sc - cs
            matrix[...,i,k] =  sj * cc + ss
            matrix[...,j,i] =  cj * sk
            matrix[...,j,j] =  sj * ss + cc
            matrix[...,j,k] =  sj * cs - sc
            matrix[...,k,i] = -sj
            matrix[...,k,j] =  cj * si
            matrix[...,k,k] =  cj * ci

        return matrix

    @staticmethod
    def euler_from_matrix(matrix, axes='rzxz'):
        """Return Euler angles from rotation matrix for specified axis sequence.

        axes : One of 24 axis sequences as string or encoded tuple

        Note that many Euler angle triplets can describe one matrix.

        >>> R0 = euler_matrix(1, 2, 3, 'syxz')
        >>> al, be, ga = euler_from_matrix(R0, 'syxz')
        >>> R1 = euler_matrix(al, be, ga, 'syxz')
        >>> np.allclose(R0, R1)
        True
        >>> angles = (4*np.pi) * (np.random.random(3) - 0.5)
        >>> for axes in _AXES2TUPLE.keys():
        ...    R0 = euler_matrix(axes=axes, *angles)
        ...    R1 = euler_matrix(axes=axes, *euler_from_matrix(R0, axes))
        ...    if not np.allclose(R0, R1): print(axes, "failed")

        """

        try:
            (firstaxis, parity, repetition,
                                frame) = Quaternion._AXES2TUPLE[axes.lower()]

        except (AttributeError, KeyError):
            Quaternion._TUPLE2AXES[axes]  # validation
            firstaxis, parity, repetition, frame = axes

        i = firstaxis
        j = Quaternion._NEXT_AXIS[i+parity]
        k = Quaternion._NEXT_AXIS[i-parity+1]

        matrix = np.asfarray(matrix)[np.newaxis]
        if repetition:
            sy = np.sqrt(matrix[...,i,j]**2 + matrix[...,i,k]**2)

            ax = np.arctan2(matrix[...,i,j],  matrix[...,i,k])
            ay = np.arctan2(sy,               matrix[...,i,i])
            az = np.arctan2(matrix[...,j,i], -matrix[...,k,i])

            mask = (sy <= Quaternion.EPSILON)
            if np.any(mask):
                ax[mask] = np.arctan2(-matrix[...,j,k], matrix[...,j,j])
                ay[mask] = np.arctan2( sy,              matrix[...,i,i])
                az[mask] = 0.

        else:
            cy = np.sqrt(matrix[...,i,i]**2 + matrix[...,j,i]**2)

            ax = np.arctan2( matrix[...,k,j], matrix[...,k,k])
            ay = np.arctan2(-matrix[...,k,i], cy)
            az = np.arctan2( matrix[...,j,i], matrix[...,i,i])

            mask = (cy <= Quaternion.EPSILON)
            if np.any(mask):
                ax[mask] = np.arctan2(-matrix[...,j,k], matrix[...,j,j])[mask]
                ay[mask] = np.arctan2(-matrix[...,k,i], cy)[mask]
                az[mask] = 0.

        if parity:
            ax, ay, az = -ax, -ay, -az
        if frame:
            ax, az = az, ax

        return (ax[0] % Quaternion.TWOPI,
                ay[0] % Quaternion.TWOPI,
                az[0] % Quaternion.TWOPI)

    @staticmethod
    def from_euler(ai, aj, ak, axes='rzxz'):
        """Return quaternion from Euler angles and axis sequence.

        ai, aj, ak : Euler's roll, pitch and yaw angles
        axes : One of 24 axis sequences as string or encoded tuple

        >>> q = quaternion_from_euler(1, 2, 3, 'ryxz')
        >>> numpy.allclose(q, [0.435953, 0.310622, -0.718287, 0.444435])
        True

        """

        shape = np.shape(ai)
        assert np.shape(aj) == shape
        assert np.shape(ak) == shape

        try:
            (firstaxis, parity, repetition,
                                frame) = Quaternion._AXES2TUPLE[axes.lower()]
        except (AttributeError, KeyError):
            Quaternion._TUPLE2AXES[axes]  # validation
            firstaxis, parity, repetition, frame = axes

        i = firstaxis + 1
        j = Quaternion._NEXT_AXIS[i+parity-1] + 1
        k = Quaternion._NEXT_AXIS[i-parity] + 1

        if frame:
            ai, ak = ak, ai
        if parity:
            aj = -aj

        ai = np.asfarray(ai) / 2.
        aj = np.asfarray(aj) / 2.
        ak = np.asfarray(ak) / 2.
        ci = np.cos(ai)
        si = np.sin(ai)
        cj = np.cos(aj)
        sj = np.sin(aj)
        ck = np.cos(ak)
        sk = np.sin(ak)
        cc = ci*ck
        cs = ci*sk
        sc = si*ck
        ss = si*sk

        q = np.empty(shape + (4,))
        if repetition:
            q[...,0] = cj*(cc - ss)
            q[...,i] = cj*(cs + sc)
            q[...,j] = sj*(cc + ss)
            q[...,k] = sj*(cs - sc)
        else:
            q[...,0] = cj*cc + sj*ss
            q[...,i] = cj*sc - sj*cs
            q[...,j] = cj*ss + sj*cc
            q[...,k] = cj*cs - sj*sc

        if parity:
            q[...,j] *= -1.

        q *= np.sign(q[...,0])[...,np.newaxis]

        return Quaternion(q)

    def to_euler(self, axes='rzxz'):
        return Quaternion.euler_from_matrix(self.to_matrix(), axes)

    @staticmethod
    def from_euler_via_matrix(ai, aj, ak, axes='rzxz'):
        m = Quaternion.euler_to_matrix(ai, aj, ak, axes)
        return Quaternion.from_matrix(m)

################################################################################

