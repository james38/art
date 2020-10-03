# based on Tom MacWright's https://github.com/tmcw/deuteranopia

import numpy as np

RANGE = 256
GAMMA = 1.8
LUT_FCTR = 0.992052
LUT_ADD = 0.003974
BY = (RANGE/2 - 1)
R_CONST = [9591, 23173]
B_CONST = [-730, (RANGE**2)/2]

luts = np.empty(RANGE)
luts_inv = np.empty(RANGE)
for i in range(RANGE):
    luts[i] = (
        LUT_FCTR
        * (i / (RANGE-1))**GAMMA
    ) + LUT_ADD
    luts_inv[i] = (
        (RANGE-1)
        * (i / (RANGE-1))**(GAMMA**-1)
    )

def to_deuteranopia(rgb):
    """ Simulate deuteranopia,
    based heavily off of Color Oracle (http://colororacle.org/),
    which is derived from [Digital Video Colourmaps for
    Checking the Legibility of Displays by Dichromats]
    (http://vision.psychol.cam.ac.uk/jdmollon/papers/colourmaps.pdf)
    """
    r_lin = luts[rgb[0]]
    g_lin = luts[rgb[1]]
    b_lin = luts[rgb[2]]

    r_blind = (
        (
            (R_CONST[0] * r_lin)
            + (R_CONST[1] * g_lin)
        ) / BY
    )
    b_blind = (
        (
            (B_CONST[0] * r_lin)
            - (B_CONST[0] * g_lin)
            + (B_CONST[1] * b_lin)
        ) / BY
    )

    r_blind = max(0, min(RANGE-1, r_blind))
    b_blind = max(0, min(RANGE-1, b_blind))

    red = luts_inv[int(round(r_blind))]
    blue = luts_inv[int(round(b_blind))]

    return np.array([red, red, blue])
