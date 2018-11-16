from PIL import ImageDraw
from tools import get_ellipse_pixels, get_locality, WHITE, BLACK, RED, GREEN


def has_C_circle(instance, *, _show_area=False):
    """
    True if instance image have C circularity
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
    True if instance image have B circularities
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
    True if instance image have D belly
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


def _show_feature_area(instance, verifying_pixels, eps):
    """
    Shows feature area. Red pixels is verifying pixels. 
    Black pixels is locality of verifying pixels, 
    used for checking feature.
    Green pixels is instance.
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
