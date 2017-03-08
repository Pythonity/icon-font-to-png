# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import os
import argparse

from icon_font_to_png import IconFont, AVAILABLE_ICON_FONTS


def run(arguments):
    """Main function for command line usage"""
    parser = argparse.ArgumentParser(
        description="Exports font icons as PNG images."
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help="list all available icon names and exit"
    )
    parser.add_argument(
        '--download',
        choices=[x for x in AVAILABLE_ICON_FONTS.keys()],
        help="download latest icon font and exit"
    )

    required_group = parser.add_argument_group("required arguments")
    required_group.add_argument(
        '--ttf',
        metavar='TTF-FILE',
        type=open,
        help='path to TTF file'
    )
    required_group.add_argument(
        '--css',
        metavar='CSS-FILE',
        type=open,
        help="path to CSS file"
    )

    exp_group = parser.add_argument_group("exporting icons")
    exp_group.add_argument(
        'icons',
        type=str,
        nargs='*',
        help="names of the icons to export (or 'ALL' for all icons)"
    )
    exp_group.add_argument(
        '--size',
        type=int,
        default=16,
        help="icon size in pixels (default: 16)"
    )
    exp_group.add_argument(
        '--scale',
        type=str,
        default='auto',
        help="scaling factor between 0 and 1, or 'auto' for automatic scaling "
             "(default: auto); be careful, as setting it may lead to icons "
             "being cropped"
    )
    exp_group.add_argument(
        '--color',
        type=str,
        default='black',
        help="color name or hex value (default: black)"
    )
    exp_group.add_argument(
        '--filename',
        type=str,
        help="name of the output file (without '.png' extension); "
             "it's used as a prefix if multiple icons are exported"
    )
    exp_group.add_argument(
        '--keep_prefix',
        default=False,
        action='store_true',
        help="do not remove common icon prefix "
             "(i.e. 'fa-arrow-right' instead of 'arrow-right')"
    )

    args = parser.parse_args(arguments)

    # Parse '--download' argument first
    if args.download:
        downloader = download_icon_font(args.download, os.getcwd())
        downloader.download_files()
        print("Icon font '{name}' successfully downloaded".format(
            name=args.download)
        )
        parser.exit()

    # If not '--download', then css and tff files are required
    if not args.css or not args.ttf:
        parser.error("You have to provide CSS and TTF files")

    icon_font = IconFont(css_file=args.css.name,
                         ttf_file=args.ttf.name,
                         keep_prefix=args.keep_prefix)
    args.css.close()
    args.ttf.close()

    # Then '--list'
    if args.list:
        for icon in icon_font.css_icons.keys():
            print(icon)
        parser.exit()

    # If not '--list' or '--download', parse passed icons
    selected_icons = list()
    if not args.icons:
        parser.error("You have to pass at least one icon name")
    elif args.icons == ['ALL']:
        selected_icons = icon_font.css_icons.keys()
    else:
        for icon in args.icons:
            if (args.keep_prefix and
                    not icon.startswith(icon_font.common_prefix)):
                # Prepend icon name with prefix
                icon = icon_font.common_prefix + icon
            elif (not args.keep_prefix and
                  icon.startswith(icon_font.common_prefix)):
                # Remove prefix from icon name
                icon = icon[len(icon_font.common_prefix):]

            # Check if given icon names exist
            if icon in icon_font.css_icons:
                selected_icons.append(icon)
            else:
                parser.error("Unknown icon name '{icon}'".format(icon=icon))

    # Parse filename and remove the extension if necessary
    given_filename = args.filename or ''
    if given_filename.lower().endswith('.png'):
        given_filename = given_filename[:-4]

    # Some fonts have empty values
    # (prefix only - which we remove - for common styles)
    selected_icons = list(filter(None, selected_icons))

    # Commence exporting
    for icon in selected_icons:
        if len(selected_icons) > 1:
            # Multiple icons - treat the filename option as name prefix
            filename = '{prefix}{icon}.png'.format(
                prefix=given_filename, icon=icon,
            )
        else:
            if given_filename:
                # Use the specified filename
                filename = given_filename + '.png'
            else:
                # Use icon name as filename
                filename = str(icon) + '.png'

        print("Exporting icon '{icon}' as '{filename}'"
              "({size}x{size} pixels)".format(icon=icon,
                                              filename=filename,
                                              size=args.size))

        icon_font.export_icon(icon=icon, filename=filename, size=args.size,
                              color=args.color, scale=args.scale)

    print()
    print("All done")


# Isolated for use in wrapper scripts
def download_icon_font(icon_font, directory):
    """Download given (implemented) icon font into passed directory"""
    try:
        downloader = AVAILABLE_ICON_FONTS[icon_font]['downloader'](directory)
        downloader.download_files()
        return downloader
    except KeyError:  # pragma: no cover
        raise Exception("We don't support downloading font '{name}'".format(
            name=icon_font)
        )
