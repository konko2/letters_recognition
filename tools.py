from PIL import Image, ImageDraw


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def get_brightness(pixels, size):
    """
    Find brightness of pixel
    :param pixels: pixel values
    :param size: size of image
    :return: dictionary of brightness
    """
    brightness = {}
    for i in range(size[0]):
        for j in range(size[1]):
            Y = round(0.299 * pixels[i, j][0] + 0.587 * pixels[i, j][1] + 0.114 * pixels[i, j][2])
            brightness.update({(i, j) : Y})
    return brightness

def dilation(img):
    """
    The use of morphological operations: dilation
    :param img: PIL.Image.Image object
    :return: PIL.Image.Image object
    """
    dilation_image = Image.new('RGB', img.size, (255, 255, 255))
    _draw_dilation = ImageDraw.Draw(dilation_image)
    kernel = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    kw = 3
    kh = 3
    pixels = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            min_value = 255
            min_R = 255
            min_G = 255
            min_B = 255
            for j in range(-kh // 2, kh // 2 + 1):
                for i in range(-kw // 2, kw // 2 + 1):
                    if (((x + i) >= 0) & ((y + j) >= 0) & ((x + i) < img.size[0]) & ((y + j) < img.size[1])) & (
                            kernel[i][j] == 1):
                        Y = round(
                            0.299 * pixels[x + i, y + j][0] + 0.587 * pixels[x + i, y + j][1] + 0.114 * pixels[x + i, y + j][2])
                        if min_value > Y:
                            min_value = Y
                            min_R = pixels[x + i, y + j][0]
                            min_G = pixels[x + i, y + j][1]
                            min_B = pixels[x + i, y + j][2]
            _draw_dilation.point((x, y), (min_R, min_G, min_B))
    return dilation_image

def search_threshold_of_brightness(pixels, size):
    """
    Find the best threshold value using the Otsu method
    :param pixels: pixel values
    :param size: size of image
    :return: the best threshold value
    """
    brightness = get_brightness(pixels, size)
    histogram = {}
    for i, j in brightness.keys():
        Y = brightness[(i, j)]
        if Y in histogram.keys():
            histogram.update({Y: histogram[Y] + 1})
        else:
            histogram.update({Y: 1})

    all_intensity_sum = sum(brightness.values())

    all_pixel_count = size[0] * size[1]
    first_class_pixel_count = 0
    first_class_intensity_sum = 0

    best_thresh = 0
    best_sigma = 0.0

    for thresh in sorted(histogram.keys()):
        first_class_pixel_count += histogram[thresh]
        first_class_intensity_sum += thresh * histogram[thresh]

        first_class_prob = first_class_pixel_count / all_pixel_count
        second_class_prob = 1.0 - first_class_prob

        first_class_mean = first_class_intensity_sum / first_class_pixel_count
        if all_pixel_count - first_class_pixel_count == 0:
            break
        second_class_mean = (all_intensity_sum - first_class_intensity_sum) / (
                all_pixel_count - first_class_pixel_count)

        mean_delta = first_class_mean - second_class_mean
        sigma = first_class_prob * second_class_prob * mean_delta ** 2

        if (sigma > best_sigma):
            best_sigma = sigma
            best_thresh = thresh

    return best_thresh

def get_neighbours(pixel):
    """
    Find neighbour pixels of 'pixel'
    :param pixel: (x, y) - tuple of pixel coordinates 
    :return: set of neighbours 
    """
    x_locality = (pixel[0] - 1, pixel[0], pixel[0] + 1)
    y_locality = (pixel[1] - 1, pixel[1], pixel[1] + 1)

    neighbours = [(x, y) for x in x_locality for y in y_locality]
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
        offsets = [
            (x, y) for x in range(area_size[0] + 1) for y in range(area_size[1] + 1)
        ]
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
