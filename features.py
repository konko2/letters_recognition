from PIL import ImageDraw
from tools import get_ellipse_pixels, get_A_slopping_lines_pixels, get_locality, WHITE, BLACK, RED, GREEN


LETTERS_DETERMINATION = {
    'A': {
        'A_slopping_lines': True,
        '2_quarter_horizont_line': True,
        '3_quarter_horizont_line': True,
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
        'right_vertical_line': False,
        'upper_horizont_line': False,
        'bottom_horizont_line': False,
        'A_slopping_lines': False,
        'C_circle': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'C': {
        'C_circle': True,
        '1_quarter_horizont_line': False,
        '2_quarter_horizont_line': False,
        '3_quarter_horizont_line': False,
        '4_quarter_horizont_line': False,
        'left_vertical_line': False,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'upper_horizont_line': False,
        'bottom_horizont_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'D': {
        'D_belly': True,
        'left_vertical_line': True,
        '1_quarter_horizont_line': False,
        '2_quarter_horizont_line': False,
        '3_quarter_horizont_line': False,
        '4_quarter_horizont_line': False,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'upper_horizont_line': False,
        'bottom_horizont_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'C_circle': False,
        'hook_from_J': False
    },
    'E': {
        'left_vertical_line': True,
        '1_quarter_horizont_line': True,
        '2_quarter_horizont_line': True,
        'upper_horizont_line': True,
        'bottom_horizont_line': True,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'C_circle': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'F': {
        'left_vertical_line': True,
        '1_quarter_horizont_line': True,
        '2_quarter_horizont_line': True,
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
        '3_quarter_horizont_line': True,
        '1_quarter_horizont_line': False,
        '2_quarter_horizont_line': False,
        'left_vertical_line': False,
        'middle_vertical_line': False,
        'right_vertical_line': False,
        'upper_horizont_line': False,
        'bottom_horizont_line': False,
        'A_slopping_lines': False,
        'B_circles': False,
        'D_belly': False,
        'hook_from_J': False
    },
    'H': {
        'left_vertical_line': True,
        'right_vertical_line': True,
        '1_quarter_horizont_line': True,
        '2_quarter_horizont_line': True,
        '3_quarter_horizont_line': True,
        '4_quarter_horizont_line': True,
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
        '1_quarter_horizont_line': False,
        '2_quarter_horizont_line': False,
        '3_quarter_horizont_line': False,
        '4_quarter_horizont_line': False,
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
        'upper_horizont_line': True,
        'hook_from_J': True,
        '1_quarter_horizont_line': False,
        '2_quarter_horizont_line': False,
        '3_quarter_horizont_line': False,
        '4_quarter_horizont_line': False,
        'left_vertical_line': False,
        'right_vertical_line': False,
        'bottom_horizont_line': False,
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
    instance_pixels = set(instance.pixels)

    first_line = {(int(0.25 * size[0]), j) for j in range(int(0.75 * size[1]), size[1])}
    second_line = {(i, size[1]) for i in range(int(0.25 * size[0]), int(0.5 * size[0]))}
    verifying_pixels = first_line | second_line

    eps = min(size) // 4

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_upper_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a upper horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    verifying_pixels = {(i, 0) for i in range(size[0] + 1)}
    instance_pixels = set(instance.pixels)

    eps = min(size) // 6

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_bottom_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a bottom horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    verifying_pixels = {(i, size[1]) for i in range(size[0] + 1)}
    instance_pixels = set(instance.pixels)

    eps = min(size) // 6

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_A_slopping_lines(instance, *, _show_area=False):
    """
    True if instance image has A slopping lines
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    lines = get_A_slopping_lines_pixels(size[0], size[1])
    instance_pixels = set(instance.pixels)

    eps = min(size) // 5

    verifying_pixels = {p for p in lines if p[1] <= 5/6*size[1]}

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def _has_quarter_horizont_line(instance, quarter, *, _show_area=False):
    """
    True if instance image has a corresponding quarter of middle horizontal line,
    where parameter quarter is a sequential number of quarter.
    :param instance: recognition.Instance object
    :param quarter: integer 1, 2, 3 or 4
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    x, y = int(0.25*size[0]), int(0.5*size[1])
    verifying_pixels = {(x*(quarter - 1) + i, y) for i in range(x + 1)}
    instance_pixels = set(instance.pixels)

    eps = (size[0] // 15, size[1] // 7)

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_1_quarter_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a first quarter of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_quarter_horizont_line(instance, 1, _show_area=_show_area)


def has_2_quarter_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a second quarter of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_quarter_horizont_line(instance, 2, _show_area=_show_area)


def has_3_quarter_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a third quarter of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_quarter_horizont_line(instance, 3, _show_area=_show_area)


def has_4_quarter_horizont_line(instance, *, _show_area=False):
    """
    True if instance image has a fourth quarter of middle horizontal line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    return _has_quarter_horizont_line(instance, 4, _show_area=_show_area)


# TODO
def has_C_circle(instance, *, _show_area=False):
    """
    True if instance image has C circularity
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance 
    :return: True or False
    """
    size = instance.size
    ellipse = get_ellipse_pixels(0, 0, 20 * size[0] // 19, size[1])
    verifying_pixels = {p for p in ellipse if p[0] <= size[0]}
    instance_pixels = set(instance.pixels)

    eps = min(size) // 7

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_B_circles(instance, *, _show_area=False):
    """
    True if instance image has B circularities
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance 
    :return: True or False
    """
    size = instance.size

    a1 = 3 * size[0] // 4
    ellipse1 = get_ellipse_pixels(
        0,
        0,
        2 * a1,
        size[1] // 2
    )

    a2 = size[0]
    ellipse2 = get_ellipse_pixels(
        0,
        size[1] // 2,
        2 * a2,
        size[1]
    )

    verifying_pixels = {
        (x - a1, y) for x, y in ellipse1 if x >= a1
    } | {
        (x - a2, y) for x, y in ellipse2 if x >= a2
    }
    instance_pixels = set(instance.pixels)

    eps = min(size) // 4

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


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
    instance_pixels = set(instance.pixels)

    eps = min(size) // 4

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_left_vertical_line(instance, *, _show_area=False):
    """
    True if instance image has a left vertical line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    verifying_pixels = {(0, i) for i in range(size[1] + 1)}
    instance_pixels = set(instance.pixels)

    eps = min(size) // 6

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_middle_vertical_line(instance, *, _show_area=False):
    """
    True if instance image has a middle vertical line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    verifying_pixels = {(size[1] // 2, i) for i in range(size[1] + 1)}
    instance_pixels = set(instance.pixels)

    eps = min(size) // 6

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def has_right_vertical_line(instance, *, _show_area=False):
    """
    True if instance image has a right vertical line.
    :param instance: recognition.Instance object
    :param _show_area: if True shows area of feature for instance
    :return: True or False
    """
    size = instance.size
    verifying_pixels = {(size[0], i) for i in range(size[1] + 1)}
    instance_pixels = set(instance.pixels)

    eps = min(size) // 6

    if _show_area:
        _show_feature_area(instance, verifying_pixels, eps)

    for pixel in verifying_pixels:
        if instance_pixels.isdisjoint(get_locality(pixel, eps)):
            return False
    return True


def _show_feature_area(instance, verifying_pixels, eps):
    """
    Shows feature area. Red pixels are verifying pixels.
    Black pixels are locality of verifying pixels,
    used for checking feature.
    Green pixels are instance.
    :param instance: recognition.Instance object
    :param verifying_pixels: list of verifying pixels
    :param eps: length of verifying pixels locality
    :return: None
    """
    size = instance.size
    new_img = ImageDraw.Image.new('RGB', size, WHITE)

    for v_pixel in verifying_pixels:
        for pixel in get_locality(v_pixel, eps):
            if 0 <= pixel[0] < size[0] and 0 <= pixel[1] < size[1]:
                new_img.putpixel(pixel, BLACK)

    for pixel in verifying_pixels:
        if 0 <= pixel[0] < size[0] and 0 <= pixel[1] < size[1]:
            new_img.putpixel(pixel, RED)

    for pixel in instance.pixels:
        if 0 <= pixel[0] < size[0] and 0 <= pixel[1] < size[1]:
            new_img.putpixel(pixel, GREEN)

    new_img.show()


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
