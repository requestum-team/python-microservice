import numpy as np


def img_to_bytes(frame):
    h = frame.shape[0].to_bytes(2, 'big')
    w = frame.shape[1].to_bytes(2, 'big')

    return h + w + frame.tobytes()


def img_from_bytes(bytes):
    h = int.from_bytes(bytes[0:2], 'big')
    w = int.from_bytes(bytes[2:4], 'big')

    return np.frombuffer(bytes[4:], dtype='uint8').reshape((h, w, 3))
