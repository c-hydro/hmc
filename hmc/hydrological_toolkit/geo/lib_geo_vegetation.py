# libraries
import numpy as np


# method to compute cost f
def compute_cost_f(cn: np.ndarray = None, veg_ia: np.ndarray = None) -> np.ndarray:

    if veg_ia is None:
        veg_ia = np.array([
            603.3, 572.9, 543.8, 515.9, 489.2, 463.6, 439.2, 415.9, 393.6, 372.3,
            352.0, 332.7, 314.3, 296.8, 280.2, 264.4, 249.4, 235.2, 221.8, 209.1, 197.1,
            185.8, 175.1, 165.1, 155.6, 146.8, 138.4, 130.7, 123.4, 116.6, 110.3, 104.4,
            98.9, 93.8, 89.1, 84.7, 80.7, 77.0, 73.7, 70.5, 67.7, 65.1, 62.8, 60.6, 58.7, 56.9,
            55.3, 53.9, 52.6, 51.4, 50.4, 49.4, 48.6, 47.8, 47.1, 46.4, 45.9, 45.3, 44.8, 44.3,
            43.8, 43.3, 42.8, 42.3, 41.8, 41.2, 40.7, 40.1, 39.5, 38.8, 38.1, 37.3, 36.5, 35.7,
            34.7, 33.8, 32.8, 31.7, 30.5, 29.4, 28.1, 26.8, 25.5, 24.1, 22.6, 21.2, 19.7, 18.1,
            16.5, 14.9, 13.3, 11.7, 10.0, 8.4, 6.8, 5.2, 3.6, 2.1, 0.6, 0.1])

    rows, cols = cn.shape
    cost_f = np.zeros(shape=(rows, cols))
    for i in np.arange(0, rows):
        for j in np.arange(0, cols):
            index = int(cn[i, j])
            if (index > 0) and (index < 100):
                value = veg_ia[index]
                cost_f[i, j] = value
    return cost_f
