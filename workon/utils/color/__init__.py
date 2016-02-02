
import random


from colour import Color

def rgb_to_hex(rgb_tuple):
    assert len(rgb_tuple) == 3
    denormalized_values = tuple(map(lambda x: 256*x, rgb_tuple))
    return '#%02x%02x%02x' % denormalized_values

def generate_colors(num, from_color='#f7aabc', to_color='#404a58'):
    """
    Generate `num` distinct Hexadecimal colors
    """
    from_color = Color(from_color)
    to_color = Color(to_color)

    if num == 0:
        return []
    elif num == 1:
        return [from_color.hex]
    return list(c.hex for c in from_color.range_to(to_color, num))

