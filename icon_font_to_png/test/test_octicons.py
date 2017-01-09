# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import random

import pytest

from icon_font_to_png import icon_font


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Fixtures
@pytest.fixture(scope='module')
def octicons():
    """Create a IconFont instance from Octicons files"""
    css_file = os.path.join(BASE_DIR, 'files', 'octicons.css')
    ttf_file = os.path.join(BASE_DIR, 'files', 'octicons.ttf')
    return icon_font.IconFont(css_file=css_file, ttf_file=ttf_file)


# Tests
def test_octicons_load_icons(octicons):
    """Test Octicons icon loading"""
    assert len(octicons.css_icons) > 0


def test_octicons_prefix(octicons):
    """Test Octicons common prefix"""
    assert octicons.common_prefix == 'octicon-'


def test_octicons_export_icon(octicons):
    """Test Octicons random icon exporting"""
    icon = random.choice(list(octicons.css_icons.keys()))
    octicons.export_icon(icon=icon, size=128, export_dir='/tmp')
    octicons.export_icon(icon=icon, size=128, color='blue', export_dir='/tmp')
    octicons.export_icon(icon=icon, size=256, export_dir='/tmp')
    octicons.export_icon(icon=icon, size=256, color='blue', export_dir='/tmp')
