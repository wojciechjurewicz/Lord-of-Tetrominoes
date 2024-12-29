import numpy as np

tetrominos = {
    'I': [
        np.array([[0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]]),
        np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0,]]),
        np.array([[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
    ],
    'O': [
        np.array([[0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),
        np.array([[0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),
        np.array([[0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]]),
        np.array([[0, 2, 2, 0], [0, 2, 2, 0], [0, 0, 0, 0]])
    ],
    'T': [
        np.array([[0, 3, 0], [3, 3, 3], [0, 0, 0]]),
        np.array([[0, 3, 0], [0, 3, 3], [0, 3, 0]]),
        np.array([[0, 0, 0], [3, 3, 3], [0, 3, 0]]),
        np.array([[0, 3, 0], [3, 3, 0], [0, 3, 0]])
    ],
    'L': [
        np.array([[0, 0, 4], [4, 4, 4], [0, 0, 0]]),
        np.array([[0, 4, 0], [0, 4, 0], [0, 4, 4]]),
        np.array([[0, 0, 0], [4, 4, 4], [4, 0, 0]]),
        np.array([[4, 4, 0], [0, 4, 0], [0, 4, 0]])
    ],
    'J': [
        np.array([[5, 0, 0], [5, 5, 5], [0, 0, 0]]),
        np.array([[0, 5, 5], [0, 5, 0], [0, 5, 0]]),
        np.array([[0, 0, 0], [5, 5, 5], [0, 0, 5]]),
        np.array([[0, 5, 0], [0, 5, 0], [5, 5, 0]])
    ],
    'S': [
        np.array([[0, 6, 6], [6, 6, 0], [0, 0, 0]]),
        np.array([[0, 6, 0], [0, 6, 6], [0, 0, 6]]),
        np.array([[0, 0, 0], [0, 6, 6], [6, 6, 0]]),
        np.array([[6, 0, 0], [6, 6, 0], [0, 6, 0]])
    ],
    'Z': [
        np.array([[7, 7, 0], [0, 7, 7], [0, 0, 0]]),
        np.array([[0, 0, 7], [0, 7, 7], [0, 7, 0]]),
        np.array([[0, 0, 0], [7, 7, 0], [0, 7, 7]]),
        np.array([[0, 7, 0], [7, 7, 0], [7, 0, 0]])
    ]
}

jlstz_kicks = {
    (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, -1): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (1, 1): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, -1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (2, 1): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, -1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 1): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (0, -1): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
}

i_kicks = {
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, -1): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (1, 1): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, -1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (2, 1): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, -1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (3, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (0, -1): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
}