# ST7789V Display Controller

![pypi status](https://img.shields.io/pypi/status/st7789v)
![pypi version](https://img.shields.io/pypi/v/st7789v?label=version)
![pypi license](https://img.shields.io/pypi/l/st7789v)

A controller for the [ST7789V][spec] display, built to control
a [2-inch LCD Module][2inch] from a Raspberry Pi or similar.

This module provides better control over the RGB color modes, easier control
of the orientation and mirroring of images and an optional Image buffer.

## Hardware requirements

To use this module, you will need a screen using the [ST7789V controller][spec]
and a device with GPIO pins and an SPI bus (or implementation) which can run
Python 3. This was developped using a Raspberry Pi 4, however it should be easy
to adapt it to other platforms.

If you wish to add support for another hardware platform, please [contact me][me]!

## Software requirements

Python 3.5 or higher is required. Prior versions may work but are unsupported.

If you're running this on a Raspberry Pi, you'll need the RPi.GPIO and spidev
modules. To use a somewhat faster implementation for color conversion, you can
install NumPy. To use the BufferedDisplay class you will need PIL.

To install all of those at once:

```sh
pip3 install RPi.GPIO spidev numpy pillow
```

## Usage

You first need an implementation of `st7789v.interface.IOWrapper`, which serves
as a generic interface to the GPIO and SPI hardware implementation. If you don't
have any hardware, you can use `st7789v.interface.Dummy` which will simply log
all sent data to the console.

After opening your interface, you can pass it to a `st7789v.Display` object,
initialize it and start sending data:

```py
from st7789v.interface import RaspberryPi
from st7789v import Display

with RaspberryPi() as rpi:
    display = Display(rpi)
    display.initialize()
    display.draw_rgb_bytes([[0, 0, 255]] * 240 * 160)
```

The above code will draw a blue rectangle over the top half of the screen.
Depending on the way your screen is installed on your PCB or device, it may
not appear on the top side, you will have to tweak initialization parameters
for this. On the [LCD module][2inch] I own, I have to use the following to
intialize the screen correctly:

```py
display.initialize(rotation=270)
```

This has the side effect of changing the screen size from 240x320 to 320x240.

See [`examples/`](./examples) for more information.

## Buffered display usage

If you have installed `PIL`, you can instantiate `BufferedDisplay` to have an
integrated image buffer. In this case, you have to pass your initialization
parameters directly to `BufferedDisplay()` if needed, because it will create
the buffer based on those parameters.

Example usage:

```py
from st7789v.interface import RaspberryPi
from st7789v import BufferedDisplay

with RaspberryPi() as rpi:
    # Instantiante the display, and initialize it in landscape mode
    display = BufferedDisplay(rpi, rotation=270)
    # Show a black screen (empty buffer)
    display.update()
    time.sleep(0.5)
    # Draw a blue rectangle all over the buffer
    display.draw.rectangle((0, 0, 320, 240), fill='BLUE')
    # Update only the top half of the screen
    display.update_partial(0, 0, 320, 120)
```

See [`examples/`](./examples) for more information.

## OpenCV usage

There is no specific code for OpenCV integration, but the format used for the
images is quite close to the one expected by `draw_rgb_bytes`. This sample
code will work, assuming the display is in landscape mode (rotation is 90° or
270°) and the video is in 320x240 resolution:

```py
# Read a frame from a video
success, image = video.read()
# Convert from BGR to RGB
image_rgb = image[:,:,::-1]
# Send to the screen
display.draw_rgb_bytes(image_rgb)
```

## Color modes

The ST7789V chip allows for 3 color modes. By default, RGB 5-6-5 is used.
This can be changed using `Display.set_color_mode(mode)` with `mode` being
one of `444`, `565` or `666`.

The table below lists all color modes, and some technical information:

- Mode: the number to pass to `Display.set_color_mode`
- Colors: the number of available colors
- Depth: the color depth in bits
- IO: the number of bits per pixel for data transfer.
  This number is higher for RGB 6-6-6 because it is transfered as standard
  RGB 8-8-8 (24 bits), but the 2 lowest bits of each bytes are ignored.
- FPS: approximate number of frames per second, using a 320x240 MP4 video
  and OpenCV to send data to the display. These numbers are for a RPi 4.

| Mode | Colors | Depth | IO | FPS |
| ---- | ------ | ----- | -- | --- |
| 444  |   4096 | 12    | 12 | 36  |
| 565  |  65536 | 16    | 16 | 27  |
| 666  | 262144 | 18    | 24 | 18  |

## Issues

If you have any trouble using this, let me know and I'll be glad to have a look
at it. You can contact me [by mail][me] or on Discord: @Zeroji#1117.

[spec]: https://newhavendisplay.com/appnotes/datasheets/LCDs/ST7789V.pdf
[2inch]: https://www.waveshare.com/wiki/2inch_LCD_Module
[me]: mailto:zzeroji@gmail.com
