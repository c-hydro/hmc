# libraries
import numpy as np


# method to fill data holes with parameter value
def fill_holes_with_param(data: np.ndarray, terrain: np.ndarray = None,
                          param: (int, float) = None) -> np.ndarray:

    if data is None:
        raise ValueError('Data is not defined')
    if terrain is None:
        raise ValueError('Terrain is not defined')

    indexes = np.where((data < 0) & (terrain >= 0))
    data[indexes] = param

    holes = indexes[0].shape[0]

    return data, holes
