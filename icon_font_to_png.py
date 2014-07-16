#!/usr/bin/env python

#
# icon_font_to_png.py
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
    icons = {}
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

        if common_prefix is None:
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
                    icons[name] = uchr(int(val[1:], 16))

    common_prefix = common_prefix or ''

    if strip_prefix and len(common_prefix) > 0:
        nonprefixed_icons = {}
        for name in icons.keys():
            nonprefixed_icons[name[len(common_prefix):]] = icons[name]
        icons = nonprefixed_icons

    return icons, common_prefix

def export_icon(icons, icon, size, filename, ttf_file, color, scale):
    # If the desired icon size is less than 150x150 pixels, we will first create
    # a 150x150 pixels image and then scale it down. This way it's much less
    # likely that the edges of the icon end up cropped.
    target_size = size
    size = max(150, target_size)

    image = Image.new("RGBA", (size, size), color=(0,0,0,0))
    draw = ImageDraw.Draw(image)

    if scale == "auto":
        scale_factor = 1
    else:
        scale_factor = float(scale)

    try:
        # Initialize font
        font = ImageFont.truetype(ttf_file, int(size * scale_factor))
    except IOError:
        print >> sys.stderr, ("Error: Font file (%s) can't be opened"
            % (ttf_file))
        exit(1)

    # Determine the desired size for the font.
    #
    # If auto-scaling is enabled, we need to make sure the resulting graphic
    # fits inside the boundary. The values are rounded and may be off by a pixel
    # or two, so we may need to do a few iterations. The use of a decrementing
    # multiplication factor protects us from getting into an infinite loop.

    iteration = 0
    factor = 1

    while True:
        width, height = draw.textsize(icons[icon], font=font)

        # Not auto-scaling?
        if scale != "auto":
            break

        dim = max(width, height)
        if dim > size:
            font = ImageFont.truetype(ttf_file, int(size * size/dim * factor))
        else:
            # The graphic fits, we're done
            break

        # Adjust the factor every two iterations
        iteration += 1
        if iteration % 2 == 0:
            factor *= 0.99

    draw.text((float(size - width) / 2, float(size - height) / 2), icons[icon],
        font=font, fill=color)

    # Get bounding box
    bbox = image.getbbox()

    # Create an alpha mask
    imagemask = Image.new("L", (size, size), 0)
    drawmask = ImageDraw.Draw(imagemask)

    # Draw the icon on the mask
    drawmask.text((float(size - width) / 2, float(size - height) / 2),
        icons[icon], font=font, fill=255)

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

    # Scale the image to the target size (if necessary)
    if target_size != size:
        outimage = outimage.resize((target_size, target_size), Image.ANTIALIAS)

    # Save file
    outimage.save(filename)

def run(argv):
    parser = argparse.ArgumentParser(
            description="Exports font icons as PNG images.")

    parser.add_argument("ttf_file", metavar="ttf-file", type=str,
        help="the name of the TTF file")
    parser.add_argument("css_file", metavar="css-file", type=str,
        help="the name of the CSS file")
    exp_group = parser.add_argument_group('exporting icons')
    exp_group.add_argument("icon", type=str, nargs="*",
        help="the name(s) of the icon(s) to export (or \"ALL\" for all icons)")
    exp_group.add_argument("--color", type=str, default="black",
        help="color (HTML color code or name, default: black)")
    exp_group.add_argument("--filename", type=str,
        help="the name of the output file, ending with \".png\" (if multiple " +
        "icons are exported, the value of this option is used as a prefix)")
    exp_group.add_argument("--keep-prefix", action="store_true", default=False,
        help="do not remove common icon prefix")
    exp_group.add_argument("--scale", type=str, default="1",
        help="scale (a scaling factor between 0 and 1, or \"auto\" for " +
            "automatic scaling, default: 1)")
    exp_group.add_argument("--size", type=int, default=16,
        help="icon size in pixels (default: 16)")
    list_group = parser.add_argument_group('listing icon names')
    list_group.add_argument("--list", action="store_true", default=False,
        help="list available icon names and exit")

    args = parser.parse_args(argv)

    icons, common_prefix = load_css(args.css_file, not args.keep_prefix)

    if args.list:
        for icon in sorted(icons.keys()):
            print(icon)
        exit(0)

    if not args.icon:
        # No icon name specified, and no --list
        parser.print_usage()
        exit(1)

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

        export_icon(icons=icons, icon=icon, size=args.size, filename=filename,
            ttf_file=args.ttf_file, color=args.color, scale=args.scale)

if __name__ == '__main__':
    run(sys.argv[1:])
