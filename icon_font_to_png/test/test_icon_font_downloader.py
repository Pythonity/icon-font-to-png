from __future__ import unicode_literals

import pytest
import os
import tempfile

from icon_font_to_png.icon_font_downloader import (
    FontAwesomeDownloader, OcticonsDownloader
)


# Font Awesome
def test_font_awesome():
    """Test initializing Font Awesome Downloader"""
    # With directory
    obj = FontAwesomeDownloader(tempfile.mkdtemp())
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    # Without directory
    obj = FontAwesomeDownloader()
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)


def test_font_awesome_latest_version_number():
    """Test that getting latest version number"""
    obj = FontAwesomeDownloader(tempfile.mkdtemp())
    assert obj.get_latest_version_number()


# Octicons
def test_octicons():
    """Test initializing Octicons Downloader"""
    # With directory
    obj = OcticonsDownloader(tempfile.mkdtemp())
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    # Without directory
    obj = OcticonsDownloader()
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)


def test_octicons_latest_version_number():
    """Test that getting latest version number"""
    obj = OcticonsDownloader(tempfile.mkdtemp())
    assert obj.get_latest_version_number()
