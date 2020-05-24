"""Define color manipulation functions."""
import itertools
import numpy as np
try:
    NUMPY_AVAILABLE = True
except ModuleNotFoundError:
    NUMPY_AVAILABLE = False


def bytes_to_rgb_444(image_data):
    """Convert list of RGB tuples to RGB 4-4-4 bytes."""
    if len(image_data) % 2:
        image_data = image_data + [(0, 0, 0)]
    data = bytearray(len(image_data) * 3 // 2)
    for i in range(len(image_data)//2):
        rgb_a, rgb_b = image_data[i*2], image_data[i*2+1]
        data[i*3] = rgb_a[0] & 0xf0 | rgb_a[1] >> 4 & 0x0f
        data[i*3+1] = rgb_a[2] & 0xf0 | rgb_b[0] >> 4 & 0x0f
        data[i*3+2] = rgb_b[1] & 0xf0 | rgb_b[2] >> 4 & 0x0f
    return data


def bytes_to_rgb_444_np(image_data):
    """Convert list of RGB tuples to RGB 4-4-4 bytes using numpy."""
    image = image_data if isinstance(
        image_data, np.ndarray) else np.asarray(image_data, dtype=np.uint8)
    if len(image) % 2:
        image.resize(len(image) + 1, 3)
    array = np.empty((len(image) // 2, 3), dtype=np.uint8)
    array[:, 0] = np.bitwise_or(np.bitwise_and(image[0::2, 0], 0xf0),
                                np.bitwise_and(np.right_shift(image[0::2, 1], 4), 0x0f))
    array[:, 1] = np.bitwise_or(np.bitwise_and(image[0::2, 2], 0xf0),
                                np.bitwise_and(np.right_shift(image[1::2, 0], 4), 0x0f))
    array[:, 2] = np.bitwise_or(np.bitwise_and(image[1::2, 1], 0xf0),
                                np.bitwise_and(np.right_shift(image[1::2, 2], 4), 0x0f))
    return array.flatten().tobytes()


def bytes_to_rgb_565(image_data):
    """Convert list of RGB tuples to RGB 5-6-5 bytes."""
    data = bytearray(len(image_data) * 2)
    i = 0
    for r, g, b in image_data:
        data[i] = r & 0xf8 | g >> 5 & 0x07
        data[i+1] = g << 3 & 0xe0 | b >> 3 & 0x1f
        i += 2
    return data


def bytes_to_rgb_565_np(image_data):
    """Convert list of RGB tuples to RGB 5-6-5 bytes using numpy."""
    image = image_data if isinstance(
        image_data, np.ndarray) else np.asarray(image_data, dtype=np.uint8)
    array = np.empty((len(image_data), 2), dtype=np.uint8)
    array[:, 0] = np.bitwise_or(np.bitwise_and(image[:, 0], 0xf8),
                                np.bitwise_and(np.right_shift(image[:, 1], 5), 0x07))
    array[:, 1] = np.bitwise_or(np.bitwise_and(np.left_shift(
        image[:, 1], 3), 0xe0), np.bitwise_and(np.right_shift(image[:, 2], 3), 0x1f))
    return array.flatten().tobytes()


def bytes_to_rgb_666(image_data):
    """Convert list of RGB tuples to RGB 6-6-6 bytes."""
    return bytes(itertools.chain.from_iterable(image_data))


def bytes_to_rgb_666_np(image_data):
    """Convert list of RGB tuples to RGB 6-6-6 bytes using numpy."""
    image = image_data if isinstance(
        image_data, np.ndarray) else np.asarray(image_data, dtype=np.uint8)
    return image.flatten().tobytes()


def image_to_rgb_444(image):
    """Convert PIL image to RGB 4-4-4."""
    return bytes.fromhex(image.tobytes().hex()[::2])


def image_to_rgb_565(image):
    """Convert PIL image to RGB 5-6-5."""
    return bytes_to_rgb_565(image.getdata())


def image_to_rgb_666(image):
    """Convert PIL image to RGB 6-6-6."""
    return image.tobytes()


# COLMOD mode ID, bytes per 2 pixels, converter func
MODES = {
    444: {'id': 0x03, 'bytes2': 3, 'func': bytes_to_rgb_444_np if NUMPY_AVAILABLE else bytes_to_rgb_444, 'image': image_to_rgb_444},
    565: {'id': 0x05, 'bytes2': 4, 'func': bytes_to_rgb_565_np if NUMPY_AVAILABLE else bytes_to_rgb_565, 'image': image_to_rgb_565},
    666: {'id': 0x06, 'bytes2': 6, 'func': bytes_to_rgb_666_np if NUMPY_AVAILABLE else bytes_to_rgb_666, 'image': image_to_rgb_666},
}

if __name__ == "__main__":
    import random
    import timeit
    from PIL import Image
    sample_image = Image.new('RGB', (240, 320))
    for y in range(320):
        for x in range(240):
            sample_image.putpixel((x, y), (random.randint(0, 255),
                                           random.randint(0, 255), random.randint(0, 255)))
    sample = list(sample_image.getdata())

    for func, n in ((bytes_to_rgb_444, 20), (bytes_to_rgb_565, 20), (bytes_to_rgb_666, 200),
                    (bytes_to_rgb_444_np, 20), (bytes_to_rgb_565_np, 20), (bytes_to_rgb_666_np, 20)):
        print('Calling %s %d times:' % (func.__name__, n))
        res = timeit.timeit(lambda f=func: f(sample), number=n)
        print('Total time: %03g\tTime per iter: %03g' % (res, res/n))

    for func, n in ((image_to_rgb_444, 1000), (image_to_rgb_565, 20), (image_to_rgb_666, 1000)):
        print('Calling %s %d times:' % (func.__name__, n))
        res = timeit.timeit(lambda f=func: f(sample_image), number=n)
        print('Total time: %03g\tTime per iter: %03g' % (res, res/n))
