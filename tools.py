import os
from collections import Counter
from itertools import product

from PIL import Image, ImageDraw


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)


def get_brightness(img):
    """
    Find brightness level of each pixel
    :param img: PIL.Image.Image object
    :return: dictionary with tuple of pixels coordinates as keys and brightness level as values
    """
    pixels = img.load()
    brightness = dict()
    for i, j in product(*(range(s) for s in img.size)):
        brightness[(i, j)] = round(sum(p * c for p, c in zip(pixels[i, j], (0.299, 0.587, 0.114))))

    return brightness


def expand_black_areas(img):
    """
    Expand black areas of image
    :param img: PIL.Image.Image object
    :return: PIL.Image.Image object
    """
    new_img = img.copy()
    pixels = new_img.load()
    size = img.size

    edge_pixels = set()
    for i, j in product(*(range(s) for s in size)):
        if pixels[i, j] == BLACK:
            edge_pixels.update(get_neighbours([i, j]))

    edge_pixels = [(i, j) for i, j in edge_pixels if 0 <= i < size[0] and 0 <= j < size[1]]

    for i, j in edge_pixels:
        pixels[i, j] = BLACK

    return new_img


def find_brightness_threshold(brightness):
    """
    Find the best threshold value using the Otsu method
    :param brightness: dictionary with tuple of pixels coordinates as keys and brightness level as values
    :return: the best threshold value
    """
    histogram = Counter(val for pix, val in brightness.items())

    all_intensity_sum = sum(brightness.values())
    all_pixel_count = len(brightness)

    first_class_pixel_count = 0
    first_class_intensity_sum = 0

    best_thresh = 0
    best_sigma = 0

    for thresh in sorted(histogram.keys())[:-1]:
        first_class_pixel_count += histogram[thresh]
        first_class_intensity_sum += thresh * histogram[thresh]
        first_class_prob = first_class_pixel_count / all_pixel_count
        first_class_mean = first_class_intensity_sum / first_class_pixel_count

        second_class_pixel_count = all_pixel_count - first_class_pixel_count
        second_class_intensity_sum = all_intensity_sum - first_class_intensity_sum
        second_class_prob = 1 - first_class_prob
        second_class_mean = second_class_intensity_sum / second_class_pixel_count

        mean_delta = first_class_mean - second_class_mean
        sigma = first_class_prob * second_class_prob * mean_delta ** 2

        if sigma > best_sigma:
            best_sigma = sigma
            best_thresh = thresh

    return best_thresh


def get_neighbours(pixel):
    """
    Find neighbour pixels of 'pixel'
    :param pixel: (x, y) - tuple of pixel coordinates 
    :return: set of neighbours 
    """
    pixel = tuple(pixel)
    neighbours = list(product(
        (pixel[0] - 1, pixel[0], pixel[0] + 1),
        (pixel[1] - 1, pixel[1], pixel[1] + 1)
    ))
    neighbours.remove(pixel)
    return neighbours


def get_locality(pixel, area_size):
    """
    Finding locality of pixel by given area size.
    If area_size is integer, returns round according to metric r = x + y.
    If area_size is tuple, returns rectangle locality
    with length = 2*area_size[0] and high = 2*area_size[1].
    :param pixel: tuple of pixel coordinates
    :param area_size: integer or tuple value depending on which type of locality is needed
    :return: list of pixels that belongs to this locality
    """
    locality = set()

    try:
        area_size = tuple(iter(area_size))
        offsets = product(*(range(s + 1) for s in area_size))
    except TypeError:
        offsets = [
            (x, y) for x in range(area_size + 1) for y in range(area_size + 1 - x)
        ]

    for x_offset, y_offset in offsets:
        locality.update([
            (pixel[0] + x_offset, pixel[1] + y_offset),
            (pixel[0] - x_offset, pixel[1] + y_offset),
            (pixel[0] + x_offset, pixel[1] - y_offset),
            (pixel[0] - x_offset, pixel[1] - y_offset)
        ])
    return [p for p in locality if p[0] >= 0 and p[1] >= 0]


def get_pixels_with_color(img, color):
    """
    Find all pixels with given color
    :param img: PIL.Image.Image object
    :param color: Color value
    :return: List of pixels
    """
    pix_data, size = img.load(), img.size
    return [
        (x, y) for x in range(size[0]) for y in range(size[1]) if pix_data[x, y] == color
    ]


def get_ellipse_pixels(x_min, y_min, x_max, y_max):
    """
    Finding pixels of ellipse in given rectangle
    :param x_min: x value of left upper point of bbox
    :param y_min: y value of left upper point of bbox
    :param x_max: x value of right bottom point of bbox
    :param y_max: y value of right bottom point of bbox
    :return: list of ellipse pixels 
    """
    _img = Image.new('RGB', (x_max+1, y_max+1), WHITE)
    _draw = ImageDraw.Draw(_img)

    _draw.ellipse(
        (x_min, y_min, x_max, y_max),
        fill=WHITE,
        outline=BLACK
    )
    return get_pixels_with_color(_img, BLACK)


def get_A_slopping_lines_pixels(x_max, y_max):
    _img = Image.new('RGB', (x_max, y_max), WHITE)
    _draw = ImageDraw.Draw(_img)

    _draw.line(
        (0, y_max, 0.5*x_max, 0),
        fill=BLACK
    )
    _draw.line(
        (x_max, y_max, 0.5 * x_max, 0),
        fill=BLACK
    )

    return get_pixels_with_color(_img, BLACK)


def get_package_dir_path():
    filename_start_index = __file__.rfind(os.sep)
    return __file__[:filename_start_index]
