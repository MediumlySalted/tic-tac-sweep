import colorsys

class Color:
    def __init__(self, h, s, v):
        self.hue = h / 360
        self.saturation = s / 100
        self.value = v / 100
        self.hsv = (self.hue, self.saturation, self.value)

    def __str__(self):
        rgb = colorsys.hsv_to_rgb(*self.hsv)
        return self.hexify(rgb)

    def hexify(self, val):
        hex_value = '#' + str(hex(int(val[0] * 256)))[2:] + str(hex(int(val[1] * 256)))[2:] + str(hex(int(val[2] * 256)))[2:]
        return hex_value

    def dark(self, dark_value=0.9):
        rgb = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value * dark_value)
        return self.hexify(rgb)