#!/usr/bin/env python

#
# icon-font-to-png.py
#
# Exports font icons as PNG images.
#
# Copyright (c) 2014 Michal Wojciechowski (http://odyniec.net/)
#

import sys, argparse, re
from os import path, access, R_OK
from PIL import Image, ImageFont, ImageDraw
import tinycss

# Support Unicode literals with both Python 2 and 3
if sys.version < '3':
    import codecs
    def u(x):
        return codecs.unicode_escape_decode(x)[0]

    def uchr(x):
        return unichr(x)
else:
    def u(x):
        return x

    def uchr(x):
        return chr(x)

def load_css(filename, strip_prefix):
    new_icons = {}
    parser = tinycss.make_parser("page3")
    stylesheet = parser.parse_stylesheet_file(filename)

    common_prefix = None

    is_icon = re.compile(u("\.(.*):before,?"))

    for rule in stylesheet.rules:
        selector = rule.selector.as_css()

        if not is_icon.match(selector):
            continue

        if not common_prefix:
            common_prefix = selector
        else:
            common_prefix = path.commonprefix((common_prefix, selector))

        for match in is_icon.finditer(selector):
            name = match.groups()[0]
            for declaration in rule.declarations:
                if declaration.name == u"content":
                    val = declaration.value.as_css()
                    if re.match("^['\"].*['\"]$", val):
                        val = val[1:-1]
                    new_icons[name] = uchr(int(val[1:], 16))

    if strip_prefix:
        for name in new_icons.keys():
            new_icons[name[len(common_prefix)-1:]] = new_icons.pop(name)
    
    return new_icons

def export_icon(icon, size, filename, font, color):
    image = Image.new("RGBA", (size, size), color=(0,0,0,0))

    draw = ImageDraw.Draw(image)

    # Initialize font
    font = ImageFont.truetype(font, size)

    # Determine the dimensions of the icon
    width,height = draw.textsize(icons[icon], font=font)

    draw.text(((size - width) / 2, (size - height) / 2), icons[icon],
            font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()

    # Create an alpha mask
    imagemask = Image.new("L", (size, size), 0)
    drawmask = ImageDraw.Draw(imagemask)

    # Draw the icon on the mask
    drawmask.text(((size - width) / 2, (size - height) / 2), icons[icon],
        font=font, fill=255)

    # Create a solid color image and apply the mask
    iconimage = Image.new("RGBA", (size,size), color)
    iconimage.putalpha(imagemask)

    if bbox:
        iconimage = iconimage.crop(bbox)

    borderw = int((size - (bbox[2] - bbox[0])) / 2)
    borderh = int((size - (bbox[3] - bbox[1])) / 2)

    # Create output image
    outimage = Image.new("RGBA", (size, size), (0,0,0,0))
    outimage.paste(iconimage, (borderw,borderh))

    # Save file
    outimage.save(filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="Exports font icons as PNG images.")

    parser.add_argument("ttf_file", metavar="ttf-file", type=str,
        help="The name of the TTF file")
    parser.add_argument("css_file", metavar="css-file", type=str,
        help="The name of the CSS file")
    parser.add_argument("icon", type=str, nargs="+",
        help="The name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    parser.add_argument("--keep-prefix", action="store_true", default=False,
        help="Do not remove common icon prefix")

    args = parser.parse_args()

    icons = load_css(args.css_file, not args.keep_prefix)
