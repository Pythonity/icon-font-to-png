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
    common_prefix = None
    parser = tinycss.make_parser("page3")
    try:
        stylesheet = parser.parse_stylesheet_file(filename)
    except IOError:
        print >> sys.stderr, ("Error: CSS file (%s) can't be opened"
            % (filename))
        exit(1)

    is_icon = re.compile(u("\.(.*):before,?"))

    for rule in stylesheet.rules:
        selector = rule.selector.as_css()

        if not is_icon.match(selector):
            continue

        if not common_prefix:
            common_prefix = selector[1:]
        else:
            common_prefix = path.commonprefix((common_prefix, selector[1:]))

        for match in is_icon.finditer(selector):
            name = match.groups()[0]
            for declaration in rule.declarations:
                if declaration.name == u"content":
                    val = declaration.value.as_css()
                    # Strip quotation marks
                    if re.match("^['\"].*['\"]$", val):
                        val = val[1:-1]
                    new_icons[name] = uchr(int(val[1:], 16))

    if strip_prefix:
        for name in new_icons.keys():
            new_icons[name[len(common_prefix):]] = new_icons.pop(name)
    
    return (new_icons, common_prefix)

def export_icon(icon, size, filename, ttf_file, color):
    image = Image.new("RGBA", (size, size), color=(0,0,0,0))

    draw = ImageDraw.Draw(image)

    try:
        # Initialize font
        font = ImageFont.truetype(ttf_file, size)
    except IOError:
        print >> sys.stderr, ("Error: Font file (%s) can't be opened"
            % (ttf_file))
        exit(1)

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
        help="the name of the TTF file")
    parser.add_argument("css_file", metavar="css-file", type=str,
        help="the name of the CSS file")
    parser.add_argument("icon", type=str, nargs="+",
        help="the name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    parser.add_argument("--color", type=str, default="black",
            help="color (HTML color code or name, default: black)")
    parser.add_argument("--filename", type=str,
        help="the name of the output file, ending with \".png\" (if multiple " +
        "icons are exported, the value of this option is used as a prefix)")
    parser.add_argument("--keep-prefix", action="store_true", default=False,
        help="do not remove common icon prefix")
    parser.add_argument("--list", action="store_true", default=False,
        help="list available icon names and exit")
    parser.add_argument("--size", type=int, default=16,
        help="icon size in pixels (default: 16)")

    args = parser.parse_args()

    (icons, common_prefix) = load_css(args.css_file, not args.keep_prefix)

    if args.list:
        for icon in sorted(icons.keys()):
            print(icon)
        exit(0)

    if args.icon == [ "ALL" ]:
        # Export all icons
        selected_icons = sorted(icons.keys())
    else:
        selected_icons = []

        # One or more icon names were given
        for icon in args.icon:
            if args.keep_prefix and not icon.startswith(common_prefix):
                # Prepend icon name with prefix
                icon = common_prefix + icon
            elif not args.keep_prefix and icon.startswith(common_prefix):
                # Remove prefix from icon name
                icon = icon[len(common_prefix):]

            if icon in icons:
                selected_icons.append(icon)
            else:
                print >> sys.stderr, "Error: Unknown icon name (%s)" % (icon)
                exit(1)

    # Commence exporting
    for icon in selected_icons:
        if len(selected_icons) > 1:
            # Multiple icons -- treat the filename option as name prefix
            filename = (args.filename or "") + icon + ".png"
        else:
            # One icon
            if args.filename:
                # Use the specified filename
                filename = args.filename
            else:
                # Use icon name as filename
                filename = icon + ".png"

        print("Exporting icon \"%s\" as %s (%ix%i pixels)" %
            (icon, filename, args.size, args.size))

        export_icon(icon, args.size, filename, args.ttf_file, args.color)
