WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
