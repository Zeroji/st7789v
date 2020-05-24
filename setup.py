import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="st7789v-Zeroji",
    version="0.1.0",
    author="Zeroji",
    author_email="zzeroji@gmail.com",
    description="Raspberry Pi module for ST7789V display",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zeroji/st7789v",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.5',
)
