# Icon Font to PNG
[![Build Status](https://img.shields.io/travis/Pythonity/icon-font-to-png.svg)][if2p travis]
[![PyPI Version](https://img.shields.io/pypi/v/icon_font_to_png.svg)][if2p pypi]
[![Python Versions](https://img.shields.io/pypi/pyversions/icon_font_to_png.svg)][if2p pypi]
[![License](https://img.shields.io/github/license/Pythonity/icon-font-to-png.svg)][license]

Python script (and library) for easy and simple export of icons from web
icon fonts (e.g. Font Awesome, Octicons) as PNG images. The best part is
the provided shell script, but you can also use it's functionality
directly in your (*probably awesome*) Python project.

There's also `font-awesome-to-png` script for backwards compatibility
with the [first][odyniec fa2p] iteration of the concept.

## Installation
Make sure you have required packages for [Pillow installation][pillow].

With `PyPI` (recommended):
```
$ pip install icon_font_to_png
```

With `git clone`:
```
$ git clone https://github.com/Pythonity/icon-font-to-png
$ pip install -r icon-font-to-png/requirements.txt
$ cd icon-font-to-png/bin
```

### OS X
As reported [here][if2p osx], to install it on OS X:
```
$ pip install icon_font_to_png --ignore-installed six
```

## Usage
```
usage: icon-font-to-png [-h] [--list] [--download {font-awesome,octicons}]
                        [--ttf TTF-FILE] [--css CSS-FILE] [--size SIZE]
                        [--scale SCALE] [--color COLOR] [--filename FILENAME]
                        [--keep_prefix]
                        [icons [icons ...]]

Exports font icons as PNG images.

optional arguments:
  -h, --help            show this help message and exit
  --list                list all available icon names and exit
  --download {font-awesome,octicons}
                        download latest icon font and exit

required arguments:
  --ttf TTF-FILE        path to TTF file
  --css CSS-FILE        path to CSS file

exporting icons:
  icons                 names of the icons to export (or 'ALL' for all icons)
  --size SIZE           icon size in pixels (default: 16)
  --scale SCALE         scaling factor between 0 and 1, or 'auto' for
                        automatic scaling (default: auto); be careful, as
                        setting it may lead to icons being cropped
  --color COLOR         color name or hex value (default: black)
  --filename FILENAME   name of the output file (without '.png' extension);
                        it's used as a prefix if multiple icons are exported
  --keep_prefix         do not remove common icon prefix (i.e. 'fa-arrow-
                        right' instead of 'arrow-right')

```

## Examples
Download latest Font Awesome:
```
$ icon-font-to-png --download font-awesome
```

List all available icons:
```
$ icon-font-to-png --css font-awesome.css --ttf fontawesome-webfont.ttf --list
```

Export 'play' and 'stop' icons, size 64x64:
```
$ icon-font-to-png --css font-awesome.css --ttf fontawesome-webfont.ttf --size 64 play stop
```

Export all icons in blue:
```
$ icon-font-to-png --css font-awesome.css --ttf fontawesome-webfont.ttf --color blue ALL
```

Export all icons in blue, but using it's hex value:
```
$ icon-font-to-png --css font-awesome.css --ttf fontawesome-webfont.ttf --color blue '#0000ff' ALL
```

Or you can use `font-awesome-to-png`, without css and ttf arguments:
```
$ font-awesome-to-png ALL
```

## API
You can use `IconFont` (and `IconFontDownloader` for that matter)
directly inside your Python project. There's no documentation as of now,
but the code is commented and *should* be pretty straightforward to use.

But feel free to ask [me](mailto:pawel.adamczak@sidnet.info) if anything
is unclear.

## Tests
Package was tested with `pytest` and `tox` on Python 2.7 and 3.4
(see `tox.ini`).

To run tests yourself run `tox` inside the repository.

## Contributions
Package source code is available at [GitHub][if2p github].

Feel free to use, ask, fork, star, report bugs, fix them, suggest 
enhancements and point out any mistakes.

## Authors
Developed and maintained by [Pythonity][pythonity].

Original version by [Michał Wojciechowski][odyniec], refactored by 
[Paweł Adamczak][pawelad].


[if2p travis]: https://travis-ci.org/Pythonity/icon-font-to-png
[if2p pypi]: https://pypi.python.org/pypi/icon_font_to_png
[license]: https://github.com/Pythonity/icon-font-to-png/blob/master/LICENSE
[odyniec fa2p]: https://github.com/odyniec/font-awesome-to-png
[pillow]: https://pillow.readthedocs.org/en/latest/installation.html
[if2p osx]: https://github.com/Pythonity/icon-font-to-png/issues/2#issuecomment-197068427
[if2p github]: https://github.com/Pythonity/icon-font-to-png
[pythonity]: http://pythonity.com/
[odyniec]: https://github.com/odyniec
[pawelad]: https://github.com/pawelad