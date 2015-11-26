from __future__ import unicode_literals

import pytest
import os
import uuid
import tempfile

from icon_font_to_png import icon_font


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
    css_file = os.path.join('files', 'test-foo.css')
    obj = icon_font.IconFont(css_file=css_file, ttf_file=None,
                             keep_prefix=True)
    assert obj.common_prefix == 'foo-'

    css_file = os.path.join('files', 'test.css')
    obj = icon_font.IconFont(css_file=css_file, ttf_file=None,
                             keep_prefix=True)
    assert obj.common_prefix == ''
