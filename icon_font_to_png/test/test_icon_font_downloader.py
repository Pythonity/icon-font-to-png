from __future__ import unicode_literals

import pytest
import os
import tempfile

from icon_font_to_png import icon_font_downloader


# Font Awesome
def test_font_awesome():
    """Test initializing Font Awesome Downloader"""
    # With directory
    obj = icon_font_downloader.FontAwesomeDownloader(tempfile.mkdtemp())
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    # Without directory
    obj = icon_font_downloader.FontAwesomeDownloader()
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)


# Octicons
def test_octicons():
    """Test initializing Octicons Downloader"""
    # With directory
    obj = icon_font_downloader.OcticonsDownloader(tempfile.mkdtemp())
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    # Without directory
    obj = icon_font_downloader.OcticonsDownloader()
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)
