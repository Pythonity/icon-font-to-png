# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import shutil
import tempfile
import uuid

import pytest
from PIL import Image, ImageChops

from icon_font_to_png import icon_font


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Fixtures
@pytest.fixture(scope='module')
def font_awesome():
    """Create a IconFont instance from Font Awesome files"""
    css_file = os.path.join(BASE_DIR, 'files', 'font-awesome.css')
    ttf_file = os.path.join(BASE_DIR, 'files', 'fontawesome-webfont.ttf')
    return icon_font.IconFont(css_file=css_file, ttf_file=ttf_file)


# Tests
def test_init():
    """Test initializing"""
    # No arguments
    with pytest.raises(TypeError):
        icon_font.IconFont()

    # Non-existent files
    with pytest.raises(IOError):
        icon_font.IconFont(css_file=str(uuid.uuid4()),
                           ttf_file=str(uuid.uuid4()))

    obj = icon_font.IconFont(css_file=tempfile.mkstemp()[1],
                             ttf_file=tempfile.mkstemp()[1])
    assert len(obj.css_icons) == 0


def test_common_prefix():
    """Test finding out what the common prefix is"""
    css_file = os.path.join(BASE_DIR, 'files', 'test-foo.css')
    obj = icon_font.IconFont(css_file=css_file, ttf_file=None,
                             keep_prefix=True)
    assert obj.common_prefix == 'foo-'

    css_file = os.path.join(BASE_DIR, 'files', 'test.css')
    obj = icon_font.IconFont(css_file=css_file, ttf_file=None,
                             keep_prefix=True)
    assert obj.common_prefix == ''


@pytest.mark.parametrize("image,size", [
    ("rocket_16.png", 16),
    ("rocket_100.png", 100),
    ("rocket_256.png", 256),
])
def test_size(font_awesome, image, size):
    """Test size option"""
    original_file = os.path.join(BASE_DIR, 'files', image)

    font_awesome.export_icon(icon='rocket', size=size)
    exported_file = os.path.join('exported', 'rocket.png')

    img1 = Image.open(original_file)
    img2 = Image.open(exported_file)

    # Check dimensions
    assert img1.size == (size, size)
    assert img2.size == (size, size)

    # Check if the images are equal
    assert ImageChops.difference(img1, img2).getbbox() is None


@pytest.mark.parametrize("image,color", [
    ("rocket_blue.png", 'blue'),
    ("rocket_cyan.png", 'cyan'),
    ("rocket_123123.png", '#123123'),
])
def test_color(font_awesome, image, color):
    """Test color option"""
    original_file = os.path.join(BASE_DIR, 'files', image)

    font_awesome.export_icon(icon='rocket', size=16, color=color)
    exported_file = os.path.join('exported', 'rocket.png')

    img1 = Image.open(original_file)
    img2 = Image.open(exported_file)

    # Check if the images are equal
    assert ImageChops.difference(img1, img2).getbbox() is None


@pytest.mark.parametrize("image,scale", [
    ("rocket_x1.png", 1),
    ("rocket_x05.png", 0.5),
    ("rocket_auto.png", 'auto'),
])
def test_scale(font_awesome, image, scale):
    """Test scale option"""
    original_file = os.path.join(BASE_DIR, 'files', image)

    font_awesome.export_icon(icon='rocket', size=16, scale=scale)
    exported_file = os.path.join('exported', 'rocket.png')

    img1 = Image.open(original_file)
    img2 = Image.open(exported_file)

    # Check if the images are equal
    assert ImageChops.difference(img1, img2).getbbox() is None


# Teardown
def teardown_module():
    """Delete exported icons directory"""
    if os.path.isdir('exported'):
        shutil.rmtree('exported')
