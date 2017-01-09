# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import random

import pytest

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
def test_font_awesome_load_icons(font_awesome):
    """Test Font Awesome icon loading"""
    assert len(font_awesome.css_icons) > 0


def test_font_awesome_prefix(font_awesome):
    """Test Font Awesome common prefix"""
    assert font_awesome.common_prefix == 'fa-'


def test_font_awesome_export_icon(font_awesome):
    """Test Font Awesome random icon exporting"""
    icon = random.choice(list(font_awesome.css_icons.keys()))
    font_awesome.export_icon(icon, size=128, export_dir='/tmp')
    font_awesome.export_icon(icon, size=128, color='blue', export_dir='/tmp')
    font_awesome.export_icon(icon, size=256, export_dir='/tmp')
    font_awesome.export_icon(icon, size=256, color='blue', export_dir='/tmp')
