# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import shutil

import pytest

from icon_font_to_png import command_line


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# Tests
def test_list_option(capfd):
    """Test listing CSS icons"""
    css_file = os.path.join(BASE_DIR, 'files', 'test-foo.css')
    ttf_file = os.path.join(BASE_DIR, 'files', 'test.ttf')  # Required argument

    # No CSS and TTF files
    with pytest.raises(SystemExit):
        command_line.run(
            '--list'.split()
        )
    out, err = capfd.readouterr()
    assert out == ''

    # Lists correctly
    with pytest.raises(SystemExit):
        command_line.run(
            '--css {css_file} --ttf {ttf_file} --list'.format(
                css_file=css_file, ttf_file=ttf_file
            ).split()
        )
    out, err = capfd.readouterr()
    assert out == 'bar\ntest\n'

    # Lists correctly, with the prefix
    with pytest.raises(SystemExit):
        command_line.run(
            '--css {css_file} --ttf {ttf_file} --keep_prefix --list'.format(
                css_file=css_file, ttf_file=ttf_file
            ).split()
        )
    out, err = capfd.readouterr()
    assert out == 'foo-bar\nfoo-test\n'


def test_icon_export(capfd):
    """Test exporting icons (on Font Awesome files)"""
    css_file = os.path.join(BASE_DIR, 'files', 'font-awesome.css')
    ttf_file = os.path.join(BASE_DIR, 'files', 'fontawesome-webfont.ttf')

    # Export none icons
    with pytest.raises(SystemExit):
        command_line.run(
            '--css {css_file} --ttf {ttf_file}'.format(
                css_file=css_file, ttf_file=ttf_file
            ).split()
        )
    out, err = capfd.readouterr()  # For skipping stdout

    # Export one icon
    command_line.run(
        '--css {css_file} --ttf {ttf_file} github'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'github.png'))

    # Export two icons
    command_line.run(
        '--css {css_file} --ttf {ttf_file} github star'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'github.png'))
    assert os.path.isfile(os.path.join('exported', 'star.png'))

    # Export all icons
    command_line.run(
        '--css {css_file} --ttf {ttf_file} ALL'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout


def test_filename_option(capfd):
    """Test filename option"""
    css_file = os.path.join(BASE_DIR, 'files', 'font-awesome.css')
    ttf_file = os.path.join(BASE_DIR, 'files', 'fontawesome-webfont.ttf')

    # Export one icon
    command_line.run(
        '--css {css_file} --ttf {ttf_file} '
        '--filename foo github'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'foo.png'))

    # Export multiple icons
    command_line.run(
        '--css {css_file} --ttf {ttf_file} '
        '--filename foo- github star'.format(
            css_file=css_file, ttf_file=ttf_file
        ).split()
    )
    out, err = capfd.readouterr()  # For skipping stdout

    assert os.path.isfile(os.path.join('exported', 'foo-github.png'))
    assert os.path.isfile(os.path.join('exported', 'foo-star.png'))


def test_download_option(capfd):
    """Test icon font download option"""
    with pytest.raises(SystemExit):
        command_line.run(
            '--download {font_name}'.format(font_name='font-awesome').split()
        )
    out, err = capfd.readouterr()  # For skipping stdout
    assert out == "Icon font 'font-awesome' successfully downloaded\n"

    assert os.path.isfile('font-awesome.css')
    assert os.path.isfile('fontawesome-webfont.ttf')


# Teardown
def teardown_module():
    """Delete exported icons directory and downloaded FontAwesome files"""
    if os.path.isdir('exported'):
        shutil.rmtree('exported')

    if os.path.isfile('font-awesome.css'):
        os.remove('font-awesome.css')

    if os.path.isfile('fontawesome-webfont.ttf'):
        os.remove('fontawesome-webfont.ttf')
