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
        r = str(hex(int(val[0] * 255)))[2:]
        g = str(hex(int(val[1] * 255)))[2:]
        b = str(hex(int(val[2] * 255)))[2:]
        if len(r) < 2: r = '0' + r
        if len(g) < 2: g = '0' + g
        if len(b) < 2: b = '0' + b
        hex_value = '#' + r + g + b
        return hex_value

    def dark(self, dark_value=0.8):
        rgb = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value * dark_value)
        return self.hexify(rgb)