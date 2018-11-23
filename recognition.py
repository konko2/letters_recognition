from PIL import Image
from tools import WHITE, BLACK, get_neighbours, get_pixels_with_color, search_threshold_of_brightness, get_brightness, dilation


class Instance:
    def __init__(self, pixels):
        x_vals, y_vals = [set(vals) for vals in zip(*pixels)]
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)

        self.start_pix = min_x, min_y
        self.pixels = [(x - min_x, y - min_y) for x, y in pixels]
        self.size = (max_x - min_x, max_y - min_y)

    def classify(self):
        """
        If instance is similar to one of defined letters, makes an attribute 'letter', which is string representation 
        of that letter. Else attribute 'letter' take a value None
        :param self: Instance object
        :return: None
        """
        pass


def handle_image(image):
    """
    Make basic filtration: removing noise from image, turning colors into black and white.
    :param image: PIL.Image.Image object
    :return: PIL.Image.Image object
    """
    filtered_image = image.copy()
    pix = filtered_image.load()
    britghtness = get_brightness(pix, filtered_image.size)
    for i, j in britghtness.keys():
        Y = britghtness[(i, j)]
        pix[i, j] = (Y, Y, Y)

    size = filtered_image.size
    thresh_value = search_threshold_of_brightness(pix, size)
    britghtness = get_brightness(pix, image.size)
    for i, j in britghtness.keys():
        Y = britghtness[(i, j)]
        if Y > thresh_value:
            pix[i, j] = WHITE
        else:
            pix[i, j] = BLACK

    filtered_image = dilation(image)
    return filtered_image

def find_instances(img):
    """
    Find instances on the image
    :param img: PIL.Image.Image object
    :return: list of Instance objects
    """
    black_pixels = set(get_pixels_with_color(img, BLACK))
    instances = list()

    while black_pixels:
        object_pixels = set()
        next_pixels = {black_pixels.pop(), }

        while next_pixels:
            black_pixels -= next_pixels
            object_pixels.update(next_pixels)

            next_pixels = set().union(*[get_neighbours(p) for p in next_pixels])
            next_pixels &= black_pixels

        instances.append(Instance(object_pixels))

    return instances


def create_output_image(img, instances):
    """
    Creates a new image with marked classified instances
    :param img: Original PIL.Image.Image image
    :param instances: List of classified instances
    :return: New PIL.Image.Image object
    """
    pass


def find_letters(image_path):
    img = Image.open(image_path)
    filtered_img = handle_image(img)
    instances = find_instances(filtered_img)
    for instance in instances:
        instance.classify()
    result_image = create_output_image(img, instances)
    return result_image
