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
        hex_value = '#'
        for i in range(3):
            x = str(hex(int(val[i] * 255)))[2:]
            if len(x) < 2: x = '0' + x
            hex_value += x
        return hex_value

    def dark(self, dark_value=0.8):
        rgb = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value * dark_value)
        return self.hexify(rgb)