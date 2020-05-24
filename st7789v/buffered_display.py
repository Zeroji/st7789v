import re
import typing
from PIL import Image, ImageDraw
from . import colors, display

class BufferedDisplay(display.Display):
    def __init__(self, io_wrapper, rotation=0, bounds=None, **kwargs):
        disp_kw = {k:v for k,v in kwargs.items() if k in ('width', 'height')}
        super().__init__(io_wrapper, **disp_kw)
        self._init_kw = {k:v for k,v in kwargs.items() if k in ('color_mode', 'mirror', 'inverted', 'reset')}
        self._init_kw['rotation'] = rotation
        self._init_kw['bounds'] = bounds
        super().initialize(**self._init_kw)
        self.buffer = Image.new('RGB', (self.width, self.height))
        self._draw = None

    def reset(self):
        super().reset()
        super().initialize(**{**self._init_kw, 'reset': False})

    @property
    def draw(self):
        if self._draw is None:
            self._draw = ImageDraw.Draw(self.buffer)
        return self._draw

    def set_color_mode(self, colmod):
        super().set_color_mode(colmod)
        self.pil_image_to_rgb = self.color_mode['image']

    def update(self):
        if self.bounds != (0, 0, self.max_w, self.max_h):
            self.set_bounds(0, 0, self.max_w, self.max_h)
        self.command('RAMWR', self.pil_image_to_rgb(self.buffer))

    def update_partial(self, left, top, right, bottom):
        if self.bounds != (left, top, right, bottom):
            self.set_bounds(left, top, right, bottom)
        self.command('RAMWR', self.pil_image_to_rgb(self.buffer.crop((left, top, right, bottom))))

    def update_partial_rect(self, x, y, width, height):
        self.update_partial(x, y, x+width, y+height)
