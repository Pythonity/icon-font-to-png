from __future__ import unicode_literals

import pytest
import os
import tempfile

from icon_font_to_png import icon_font_downloader


# Font Awesome
def test_font_awesome():
    """Test initializing Font Awesome Downloader"""
    obj = icon_font_downloader.FontAwesomeDownloader(
        directory=tempfile.mkdtemp()
    )
    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    obj = icon_font_downloader.FontAwesomeDownloader()
    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)


# Octicons
def test_octicons():
    """Test initializing Octicons Downloader"""
    obj = icon_font_downloader.OcticonsDownloader(
        directory=tempfile.mkdtemp()
    )
    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    obj = icon_font_downloader.OcticonsDownloader()
    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)
