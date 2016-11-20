# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import re
from collections import OrderedDict

import tinycss
from PIL import Image, ImageFont, ImageDraw
from six import unichr


class IconFont(object):
    """Base class that represents web icon font"""
    def __init__(self, css_file, ttf_file, keep_prefix=False):
        """
        :param css_file: path to icon font CSS file
        :param ttf_file: path to icon font TTF file
        :param keep_prefix: whether to keep common icon prefix
        """
        self.css_file = css_file
        self.ttf_file = ttf_file
        self.keep_prefix = keep_prefix

        self.css_icons, self.common_prefix = self.load_css()

    def load_css(self):
        """
        Creates a dict of all icons available in CSS file, and finds out
        what's their common prefix.

        :returns sorted icons dict, common icon prefix
        """
        icons = dict()
        common_prefix = None
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet_file(self.css_file)

        is_icon = re.compile("\.(.*):before,?")

        for rule in stylesheet.rules:
            selector = rule.selector.as_css()

            # Skip CSS classes that are not icons
            if not is_icon.match(selector):
                continue

            # Find out what the common prefix is
            if common_prefix is None:
                common_prefix = selector[1:]
            else:
                common_prefix = os.path.commonprefix((common_prefix,
                                                      selector[1:]))

            for match in is_icon.finditer(selector):
                name = match.groups()[0]
                for declaration in rule.declarations:
                    if declaration.name == "content":
                        val = declaration.value.as_css()
                        # Strip quotation marks
                        if re.match("^['\"].*['\"]$", val):
                            val = val[1:-1]
                        icons[name] = unichr(int(val[1:], 16))

        common_prefix = common_prefix or ''

        # Remove common prefix
        if not self.keep_prefix and len(common_prefix) > 0:
            non_prefixed_icons = {}
            for name in icons.keys():
                non_prefixed_icons[name[len(common_prefix):]] = icons[name]
            icons = non_prefixed_icons

        sorted_icons = OrderedDict(sorted(icons.items(), key=lambda t: t[0]))

        return sorted_icons, common_prefix

    def export_icon(self, icon, size, color='black', scale='auto',
                    filename=None, export_dir='exported'):
        """
        Exports given icon with provided parameters.

        If the desired icon size is less than 150x150 pixels, we will first
        create a 150x150 pixels image and then scale it down, so that
        it's much less likely that the edges of the icon end up cropped.

        :param icon: valid icon name
        :param filename: name of the output file
        :param size: icon size in pixels
        :param color: color name or hex value
        :param scale: scaling factor between 0 and 1,
                      or 'auto' for automatic scaling
        :param export_dir: path to export directory
        """
        org_size = size
        size = max(150, size)

        image = Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        if scale == 'auto':
            scale_factor = 1
        else:
            scale_factor = float(scale)

        font = ImageFont.truetype(self.ttf_file, int(size * scale_factor))
        width, height = draw.textsize(self.css_icons[icon], font=font)

        # If auto-scaling is enabled, we need to make sure the resulting
        # graphic fits inside the boundary. The values are rounded and may be
        # off by a pixel or two, so we may need to do a few iterations.
        # The use of a decrementing multiplication factor protects us from
        # getting into an infinite loop.
        if scale == 'auto':
            iteration = 0
            factor = 1

            while True:
                width, height = draw.textsize(self.css_icons[icon], font=font)

                # Check if the image fits
                dim = max(width, height)
                if dim > size:
                    font = ImageFont.truetype(self.ttf_file,
                                              int(size * size/dim * factor))
                else:
                    break

                # Adjust the factor every two iterations
                iteration += 1
                if iteration % 2 == 0:
                    factor *= 0.99

        draw.text((float(size - width) / 2, float(size - height) / 2),
                  self.css_icons[icon], font=font, fill=color)

        # Get bounding box
        bbox = image.getbbox()

        # Create an alpha mask
        image_mask = Image.new("L", (size, size), 0)
        draw_mask = ImageDraw.Draw(image_mask)

        # Draw the icon on the mask
        draw_mask.text((float(size - width) / 2, float(size - height) / 2),
                       self.css_icons[icon], font=font, fill=255)

        # Create a solid color image and apply the mask
        icon_image = Image.new("RGBA", (size, size), color)
        icon_image.putalpha(image_mask)

        if bbox:
            icon_image = icon_image.crop(bbox)

        border_w = int((size - (bbox[2] - bbox[0])) / 2)
        border_h = int((size - (bbox[3] - bbox[1])) / 2)

        # Create output image
        out_image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out_image.paste(icon_image, (border_w, border_h))

        # If necessary, scale the image to the target size
        if org_size != size:
            out_image = out_image.resize((org_size, org_size), Image.ANTIALIAS)

        # Make sure export directory exists
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        # Default filename
        if not filename:
            filename = icon + '.png'

        # Save file
        out_image.save(os.path.join(export_dir, filename))
