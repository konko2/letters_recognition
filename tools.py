from PIL import Image, ImageDraw


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


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


def get_locality(pixel, distance):
    """
    Finding locality of pixel by given distance
    :param pixel: tuple of pixel coordinates
    :param distance: integer length 
    :return: list of pixels that belongs to this locality
    """
    locality = set()
    for x_offset in range(distance + 1):
        for y_offset in range(distance + 1 - x_offset):
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
