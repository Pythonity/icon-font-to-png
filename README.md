Icon Font to PNG
================

This program allows you to extract icons from an icon font (e.g. Font Awesome or
Octicons) as PNG images of specified size.

### Usage

    icon-font-to-png.py [-h] [--color COLOR] [--filename FILENAME]
                        [--keep-prefix] [--list] [--size SIZE]
                        ttf-file css-file icon [icon ...]

    positional arguments:
      ttf-file             the name of the TTF file
      css-file             the name of the CSS file
      icon                 the name(s) of the icon(s) to export (or "ALL" for all
                           icons)

    optional arguments:
      --color COLOR        Color (HTML color code or name, default: black)
      --filename FILENAME  The name of the output file (it must end with ".png").
                           If all files are exported, it is used as a prefix.
      --keep-prefix        do not remove common icon prefix
      --list               list available icon names and exit
      --size SIZE          Icon size in pixels (default: 16)
