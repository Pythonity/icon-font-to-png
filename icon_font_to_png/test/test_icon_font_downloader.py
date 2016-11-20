# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import tempfile

import pytest
from flaky import flaky

from icon_font_to_png.icon_font_downloader import (
    FontAwesomeDownloader, OcticonsDownloader
)


# Tests
@flaky
@pytest.mark.parametrize("downloader", [
    FontAwesomeDownloader,
    OcticonsDownloader,
])
def test_icon_font_downloader(downloader):
    """Test initializing Font Awesome Downloader"""
    # With directory
    obj = downloader(tempfile.mkdtemp())
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)

    # Without directory
    obj = downloader()
    obj.download_files()

    assert os.path.isfile(obj.css_path)
    assert os.path.isfile(obj.ttf_path)


@pytest.mark.parametrize("downloader", [
    FontAwesomeDownloader,
    OcticonsDownloader,
])
def test_font_awesome_latest_version_number(downloader):
    """Test that getting latest version number"""
    obj = downloader(tempfile.mkdtemp())
    assert obj.get_latest_version_number()
