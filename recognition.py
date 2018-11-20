from PIL import Image, ImageDraw
from tools import BLACK, get_neighbours, get_pixels_with_color


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


def handle_image(img):
    """
    Make basic filtration: removing noise from image, turning colors into black and white.
    :param img: PIL.Image.Image object
    :return: PIL.Image.Image object
    """

    def otsuThreshold(pixels, size):
        intensity_lager_number = 256
        histogram = [0 for i in range(intensity_lager_number)]
        for i in range(size[0]):
            for j in range(size[1]):
                Y = round(0.299 * pixels[i, j][0] + 0.587 * pixels[i, j][1] + 0.114 * pixels[i, j][2])
                histogram[Y] += 1
        all_intensity_sum = 0
        for i in range(size[0]):
            for j in range(size[1]):
                Y = round(0.299 * pixels[i, j][0] + 0.587 * pixels[i, j][1] + 0.114 * pixels[i, j][2])
                all_intensity_sum += Y

        all_pixel_count = size[0] * size[1]
        first_class_pixel_count = 0
        first_class_intensity_sum = 0

        best_thresh = 0
        best_sigma = 0.0

        max_thresh = 0
        min_thresh = 255
        for i in range(size[0]):
            for j in range(size[1]):
                Y = round(0.299 * pixels[i, j][0] + 0.587 * pixels[i, j][1] + 0.114 * pixels[i, j][2])
                if min_thresh > Y:
                    min_thresh = Y
                if max_thresh < Y:
                    max_thresh = Y

        for thresh in range(min_thresh, max_thresh + 1):
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
            sigma = first_class_prob * second_class_prob * mean_delta * mean_delta

            if (sigma > best_sigma):
                best_sigma = sigma
                best_thresh = thresh

        return best_thresh

    image = img
    pix = image.load()
    gray = ImageDraw.Draw(image)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            Y = round(0.299 * pix[i, j][0] + 0.587 * pix[i, j][1] + 0.114 * pix[i, j][2])
            gray.point((i, j), (Y, Y, Y))
    # image.save("gray.jpg", "JPEG")

    pix = image.load()
    size = image.size
    thresh_value = otsuThreshold(pix, size)
    thresh = ImageDraw.Draw(image)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            Y = round(0.299 * pix[i, j][0] + 0.587 * pix[i, j][1] + 0.114 * pix[i, j][2])
            if Y > thresh_value:
                thresh.point((i, j), (255, 255, 255))
            else:
                thresh.point((i, j), (0, 0, 0))
    # image.save("thresh.jpg", "JPEG")

    pix = image.load()
    image_copy = image.copy()
    thresh_morph = ImageDraw.Draw(image_copy)
    kernel = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    kw = 3
    kh = 3
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            min_value = 255
            min_R = 255
            min_G = 255
            min_B = 255
            for j in range(-kh // 2, kh // 2 + 1):
                for i in range(-kw // 2, kw // 2 + 1):
                    if (((x + i) >= 0) & ((y + j) >= 0) & ((x + i) < image.size[0]) & ((y + j) < image.size[1])) & (
                            kernel[i][j] == 1):
                        Y = round(
                            0.299 * pix[x + i, y + j][0] + 0.587 * pix[x + i, y + j][1] + 0.114 * pix[x + i, y + j][2])
                        if min_value > Y:
                            min_value = Y
                            min_R = pix[x + i, y + j][0]
                            min_G = pix[x + i, y + j][1]
                            min_B = pix[x + i, y + j][2]
            thresh_morph.point((x, y), (min_R, min_G, min_B))
    image = image_copy
    #image.save("bin_image.jpg", "JPEG")
    return image

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
