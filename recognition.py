from PIL import Image


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Instance:
    def __init__(self, pixels):
        min_x = min(x for x, y in pixels)
        min_y = min(y for x, y in pixels)

        self.start_pix = min_x, min_y
        self.pixels = [(x - min_x, y - min_y) for x, y in pixels]

    def classify(self):
        """
        If instance is similar to one of defined letters, makes an attribute 'letter', which is string representation 
        of that letter. Else attribute 'letter' take a value None
        :param self: Instance object
        :return: None
        """
        pass


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


def handle_image(img):
    """
    Make basic filtration: removing noise from image, turning colors into black and white.
    :param img: PIL.Image.Image object
    :return: PIL.Image.Image object
    """
    pass


def find_instances(img):
    """
    Find instances on the image
    :param img: PIL.Image.Image object
    :return: list of Instance objects
    """
    img_data = img.load()
    size = img.size
    black_pixels = {
        (x, y) for x in range(size[0]) for y in range(size[1]) if img_data[x, y] == BLACK
    }

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
