def hexColor(rgb):
    red = int(rgb[0])
    green = int(rgb[1])
    blue = int(rgb[2])
    return "#{:02x}{:02x}{:02x}".format(red, green, blue)


def generateColors(c_range, steps):
    colors = []
    colors.append(hexColor(c_range[0]))
    red = c_range[0][0]
    green = c_range[0][1]
    blue = c_range[0][2]
    for i in range(steps):
        red += (c_range[-1][0] - c_range[0][0]) / steps
        green += (c_range[-1][1] - c_range[0][1]) / steps
        blue += (c_range[-1][2] - c_range[0][2]) / steps
        colors.append(hexColor([red, green, blue]))
    colors.append(hexColor(c_range[-1]))
    return colors
