import os

from PIL import Image, ImageDraw, ImageFont

from .features import find_features, LETTERS_DETERMINATION
from .tools import WHITE, BLACK, PINK, get_neighbours, get_pixels_with_color, find_brightness_threshold, \
    get_brightness, expand_black_areas, get_package_dir_path


class Instance:
    def __init__(self, pixels):
        x_vals, y_vals = [set(vals) for vals in zip(*pixels)]
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)

        self.start_pix = min_x, min_y
        self.pixels = [(x - min_x, y - min_y) for x, y in pixels]
        self.size = (max_x - min_x + 1, max_y - min_y + 1)

    def get_resized(self, ratio):
        resized_img = Image.new('RGB', self.size, WHITE)
        for pixel in self.pixels:
            resized_img.putpixel(pixel, BLACK)

        resized_img = resized_img.resize([int(s * ratio) for s in self.size])
        brightness = get_brightness(resized_img)
        resized_pixels = {pixel for pixel, bright in brightness.items() if bright < 130}
        return Instance(resized_pixels)

    def classify(self):
        """
        If instance is similar to one of defined letters, makes an attribute 'letter', which is string representation 
        of that letter. Else attribute 'letter' takes a value None
        :param self: Instance object
        :return: None
        """
        size = self.size
        if min(size) < 10 or not 0.3 < size[1]/size[0] < 5:
            self.letter = None
            return

        ratio = 100 / max(size)
        instance_features = find_features(self.get_resized(ratio)) if ratio < 1 else find_features(self)

        for letter, letter_features in LETTERS_DETERMINATION.items():
            if set(letter_features.items()).issubset(instance_features.items()):
                self.letter = letter
                return
        self.letter = None


def handle_image(image):
    """
    Make basic filtration: removing noise from image, turning colors into black and white.
    :param image: PIL.Image.Image object
    :return: PIL.Image.Image object
    """
    filtered_image = Image.new('RGB', image.size, WHITE)
    pixels = filtered_image.load()

    brightness = get_brightness(image)
    thresh_value = find_brightness_threshold(brightness)
    for (i, j), bright in brightness.items():
        pixels[i, j] = WHITE if bright > thresh_value else BLACK

    filtered_image = expand_black_areas(filtered_image)
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
    output_img = img.copy()
    draw = ImageDraw.Draw(output_img)

    font_path = os.sep.join([get_package_dir_path(), 'OpenSans-Regular.ttf'])
    font = ImageFont.truetype(font_path, size=min(img.size) // 15)

    for instance in instances:
        if instance.letter:
            size = instance.size
            start_pix = instance.start_pix
            end_pix = (start_pix[0] + size[0], start_pix[1] + size[1])

            draw.rectangle((start_pix, end_pix), width=2, outline=PINK)
            draw.text(end_pix, instance.letter, fill=PINK, font=font)

    return output_img


def find_letters(image_path):
    img = Image.open(image_path)
    filtered_img = handle_image(img)
    instances = find_instances(filtered_img)
    for instance in instances:
            instance.classify()
    result_image = create_output_image(img, instances)
    return result_image
