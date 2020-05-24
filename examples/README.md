# ST7789V examples

**WARNING**: These examples all use the `RaspberryPi` interface in the default
GPIO / SPI configuration. If you have another pin configuration or another
device plugged in, **you could permanently damage your hardware**. Please
double-check your pin configuration before running any of these.

All examples are meant to be run from the root directly, using:

```sh
python3 -m examples.filename
```

## `backlight`

Uses the bare IOWrapper implementation to transition the backlight from 0%
to 100% over the course of 5 seconds. This doesn't send any command to the
ST7789V controller itself, and may not work if your hardware platform does
not include backlight control pins.

## `bootstrap`

Used to provide a very basic framework for REPL testing:

```python
$ python3 -im examples.bootstrap
# Use `display` to control the display, and `draw` to draw on the buffer.
>>> draw.rectangle((50, 50, 100, 100), fill='RED')
>>> display.update()
```

This module uses BufferedDisplay, and requires PIL to be installed.

## `bsod`

Displays a simple blue screen .

## `lena`

Displays the Lena picture in RGB 4-4-4, then 5-6-5, then 6-6-6.

## `off_on`

Shows a white screen, then turns off the display, turns off the backlight,
turns the display back on, and turns the backlight back on.

## `rgb`

Displays all 65536 colors of the RGB 5-6-5 mode, with 64 squares of 32x32
pixels (red on X, blue on Y, green increasing for each square), 6 squares
of full red/yellow/green/cyan/blue/magenta, and 10 32x16 shades of gray
at the bottom.

## `rgb_modes`

Displays the 3 R/G/B bands for the 3 RGB modes, showing how distinguishable
colors are in each mode. From top to bottom, there is RGB 4-4-4 (4 bits per
color), a black line, RGB 5-6-5 (5 bits for blue and red, 6 for green), a
black line, and RGB 6-6-6 with full color depth for each color.

## `rotation`

Draws red, green and blue 64x64 squares, in that order, in the top-left
corner, separated by white space. This example then iterates over all
4 rotations (0°, 90° (CW), 180°, 270° (CCW)), and again but mirrored.
It can be used to figure out the best settings for your setup.
