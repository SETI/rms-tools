import numpy as np

def from_float32(buffer):
    """Interprets an arbitrary string or NumPy array as Vax single-precision
    floating-point binary values, and returns the equivalent array in IEEE
    values."""

    # Convert the buffer to 2-byte elements
    if type(buffer) == type(''):
        pairs = np.fromstring(buffer, dtype='uint16')
        pairs = pairs.reshape(pairs.size//2, 2)
        newshape = (pairs.size//2,)
    else:
        buffer = np.asarray(buffer)
        pairs = buffer.view('uint16')
        assert pairs.shape[-1] % 2 == 0, \
               'buffer shape is incompatible with 4-byte elements'

        if buffer.itemsize == 1:
            newshape = buffer.shape[:-1] + (buffer.shape//4,)
        elif buffer.itemsize == 2:
            newshape = buffer.shape[:-1] + (buffer.shape//2,)
        elif buffer.itemsize == 4:
            newshape = buffer.shape[:-1] + (1,)
        else:
            newshape = buffer.shape + (buffer.itemsize//4,)

        if newshape[-1] == 1: newshape = newshape[:-1]

    # Perform a pairwise swap of the two-byte elements
    swapped = np.empty(pairs.shape, dtype='uint16')
    swapped[...,:] = pairs[...,::-1]

    # The results are in LSB IEEE format aside from a scale factor of four
    ieee = swapped.view('<f4') / 4.
    return ieee.reshape(newshape)

def to_float32(array):
    """Converts an arbitrary array of floating-point numbers into Vax single-
    precision, and returns the resulting array as a character string."""

    pre_swapped = (4. * array).ravel().astype('<f4')
    paired_view = pre_swapped.view('uint16')

    paired_view = paired_view.reshape((paired_view.size//2, 2))
    swapped = paired_view[:,::-1].copy()

    return swapped.tostring()
