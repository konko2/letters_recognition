from PIL import Image


class Instance:
    def classify(self):
        """
        If instance is similar to one of defined letters, makes an attribute 'letter', which is string representation 
        of that letter. Else attribute 'letter' take a value None
        :param self: Instance object
        :return: None
        """
        pass


def handle_image(img):
    """
    Make basic filtration: removing noise from image, turning colors into black and white.
    :param img: PIL.Image.Image object
    :return: PIL.Image.Image object
    """
    pass


def find_instances(img):
    """
    Find instances in image
    :param img: PIL.Image.Image object
    :return: list of Instance objects
    """
    pass


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
