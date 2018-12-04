from PIL import Image, ImageDraw

from .tools import get_ellipse_pixels, get_A_slopping_lines_pixels, get_locality, WHITE, BLACK, RED, GREEN, BLUE


LETTERS_DETERMINATION = {
    'A': {
        'A_slopping_lines': True,
        '2_part_horizont_line': True,
        'left_vertical_line': False,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'upper_horizont_line': False,
        'bottom_horizont_line': False,
        'B_circles': False,
        'C_circle': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'B': {
        'B_circles': True,
        'left_vertical_line': True,
        'middle_vertical_line': False,
    },
    'C': {
        'C_circle': True,
        '2_part_horizont_line': False,
        '3_part_horizont_line': False,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'A_slopping_lines': False,
        'B_circles': False
    },
    'D': {
        'D_belly': True,
        'left_vertical_line': True,
        '1_part_horizont_line': False,
        '2_part_horizont_line': False,
        'middle_vertical_line': False,
        'B_circles': False
    },
    'E': {
        'left_vertical_line': True,
        '1_part_horizont_line': True,
        'upper_horizont_line': True,
        'bottom_horizont_line': True,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
    },
    'F': {
        'left_vertical_line': True,
        '1_part_horizont_line': True,
        'upper_horizont_line': True,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'bottom_horizont_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'C_circle': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'G': {
        'C_circle': True,
        '3_part_horizont_line': True,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'B_circles': False,
        'D_belly': False
    },
    'H': {
        'left_vertical_line': True,
        'right_vertical_line': True,
        '1_part_horizont_line': True,
        '2_part_horizont_line': True,
        '3_part_horizont_line': True,
        'middle_vertical_line': False,
        'upper_horizont_line': False,
        'bottom_horizont_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'C_circle': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'I': {
        'middle_vertical_line': True,
        'upper_horizont_line': True,
        'bottom_horizont_line': True,
        'left_vertical_line': False,
        'right_vertical_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'C_circle': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'J': {
        'middle_vertical_line': True,
        'hook_from_J': True,
        '1_part_horizont_line': False,
        'left_vertical_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'C_circle': False,
        'D_belly': False
    }
}


def has_hook_from_J(instance, *, _show_area=False):
    """
    True if instance image has a hook from J
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    start_pix = (0, size[1] * 3 // 5)
    end_pix = (size[0] * 5 // 8, size[1])
    middle_pix = ((start_pix[0] + end_pix[0]) / 2, (start_pix[1] + end_pix[1]) / 2)
    ellipse = get_ellipse_pixels(*start_pix, *end_pix)

    verifying_pixels = {p for p in ellipse if p[1] >= middle_pix[1]}

    eps = min(size) // 6

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_upper_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a upper horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    verifying_pixels = {(i, 0) for i in range(size[0])}
    edges = size[0] // 8, size[0] * 7 // 8
    verifying_pixels = {p for p in verifying_pixels if edges[0] < p[0] < edges[1]}

    eps = (size[0] // 8, size[1] // 6)

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_bottom_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a bottom horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    verifying_pixels = {(i, size[1] - 1) for i in range(size[0])}
    edges = size[0] // 8, size[0] * 7 // 8
    verifying_pixels = {p for p in verifying_pixels if edges[0] < p[0] < edges[1]}

    eps = (size[0] // 8, size[1] // 6)

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_A_slopping_lines(instance, *, _show_area=False):
    """
    True if instance image has A slopping lines
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    lines = get_A_slopping_lines_pixels(size[0], size[1])
    verifying_pixels = {p for p in lines if p[1] <= 5/6*size[1]}

    eps = min(size) // 5

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def _has_part_horizont_line(instance, part_begin_end, *, _show_area=False):
    """
    True if instance image has a corresponding quarter of middle horizontal line,
    where parameter quarter is a sequential number of quarter.
    :param instance: recognition.Instance object
    :param quarter_num: integer 1, 2, 3 or 4
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    middle_height = size[1] // 2
    verifying_pixels = {
        (x, middle_height) for x in range(int(part_begin_end[0]*size[0]), int(part_begin_end[1]*size[0]) + 1)
    }
    edges = size[0] // 6, size[0] * 5 // 6
    verifying_pixels = {p for p in verifying_pixels if edges[0] < p[0] < edges[1]}
    instance_pixels = set(instance.pixels)

    eps = (instance.size[0] // 18, instance.size[1] // 5)

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_1_part_horizont_line(instance, *, _show_area=False):

    """
    True if instance image has the first part of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_part_horizont_line(instance, (0, 2/5), _show_area=_show_area)


def has_2_part_horizont_line(instance, *, _show_area=False):

    """
    True if instance image has the second part of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_part_horizont_line(instance, (2/5, 3/5), _show_area=_show_area)


def has_3_part_horizont_line(instance, *, _show_area=False):

    """
    True if instance image has the third part of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_part_horizont_line(instance, (3/5, 1), _show_area=_show_area)


def has_C_circle(instance, *, _show_area=False):
    """
    True if instance image has C circularity
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance 
    :return: True or False
    """
    size = instance.size

    ellipse = get_ellipse_pixels(0, 0, 20 * size[0] // 19, size[1])
    verifying_pixels = {p for p in ellipse if p[0] < size[0]}

    middle_pix = (size[0] // 2, size[1] // 2)
    bound = size[1] // 12
    optional_tail = {p for p in verifying_pixels if (
        middle_pix[0] < p[0] and
        bound <= p[1] < middle_pix[1]
    )}
    verifying_pixels -= optional_tail

    eps = min(size) * 7 // 24

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_B_circles(instance, *, _show_area=False):
    """
    True if instance image has B circularities
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance 
    :return: True or False
    """
    size = instance.size

    a1 = 3 * size[0] // 4
    ellipse1 = get_ellipse_pixels(0, 0, 2 * a1, size[1] // 2)
    upper_belly = {(x - a1, y) for x, y in ellipse1 if x >= a1}

    a2 = size[0]
    ellipse2 = get_ellipse_pixels(0, size[1] // 2, 2 * a2, size[1])
    bottom_belly = {(x - a2, y) for x, y in ellipse2 if x >= a2}

    verifying_pixels = {p for p in upper_belly | bottom_belly if p[0] >= size[0] // 10}

    eps = min(size) // 6

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_D_belly(instance, *, _show_area=False):
    """
    True if instance image has D belly
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance 
    :return: True or False
    """
    size = instance.size

    ellipse = get_ellipse_pixels(0, 0, 2 * size[0] - 1, size[1])
    verifying_pixels = {(x - size[0], y) for x, y in ellipse if x >= size[0]}

    eps = min(size) // 5

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_left_vertical_line(instance, *, _show_area=False):
    """
    True if instance image has a left vertical line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    verifying_pixels = {(0, i) for i in range(size[1] + 1)}
    edges = size[1] // 8, size[1] * 7 // 8
    verifying_pixels = {p for p in verifying_pixels if edges[0] < p[1] < edges[1]}

    eps = (size[0] // 6, size[1] // 8)

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_middle_vertical_line(instance, *, _show_area=True):
    """
    True if instance image has a middle vertical line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    verifying_pixels = {(size[0] // 2, i) for i in range(size[1] + 1)}
    edges = size[1] // 8, size[1] * 7 // 8
    verifying_pixels = {p for p in verifying_pixels if edges[0] < p[1] < edges[1]}

    eps = (size[0] // 6, size[1] // 8)

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def has_right_vertical_line(instance, *, _show_area=False):
    """
    True if instance image has a right vertical line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size

    verifying_pixels = {(size[0] - 1, i) for i in range(size[1])}
    edges = size[1] // 8, size[1] * 7 // 8
    verifying_pixels = {p for p in verifying_pixels if edges[0] < p[1] < edges[1]}

    eps = (size[0] // 6, size[1] // 8)

    return _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, _show_area=_show_area)


def _scale_feature_with_verifying_pixels(instance, verifying_pixels, eps, *, _show_area=False):
    instance_pixels = set(instance.pixels)

    if _show_area:
        showing_img = Image.new('RGB', instance.size, WHITE)
        canvas = ImageDraw.ImageDraw(showing_img)

        locality_pixels = set().union(*(get_locality(p, eps) for p in verifying_pixels))
        for pixel in locality_pixels:
            canvas.point(pixel, BLACK)

        for pixel in verifying_pixels:
            canvas.point(pixel, RED)

        for pixel in instance_pixels:
            canvas.point(pixel, GREEN)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            if _show_area:
                for locality_pixel in get_locality(pixel, eps):
                    canvas.point(locality_pixel, BLUE)
                canvas.point(pixel, RED)
                showing_img.show()
            return False

    if _show_area:
        showing_img.show()
    return True


def find_features(instance):
    """
    Scales all features for given instance
    :param instance: recognition.Instance object
    :return: Dict with feature names as keys and boolean answers as values
    """
    feature_funcs = {
        key: value for key, value in globals().items() if key.startswith('has_')
    }
    return {func_name[4:]: func(instance) for func_name, func in feature_funcs.items()}
