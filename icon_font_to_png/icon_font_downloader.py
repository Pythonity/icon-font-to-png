from __future__ import unicode_literals

import os
from abc import ABCMeta, abstractmethod

import requests
from six import with_metaclass, PY3

if PY3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


class IconFontDownloader(with_metaclass(ABCMeta)):
    """Abstract class for downloading icon font CSS and TTF files"""
    css_path = None
    ttf_path = None

    @property
    @abstractmethod
    def css_url(self):
        """Icon font CSS file URL"""

    @property
    @abstractmethod
    def ttf_url(self):
        """Icon font TTF file URL"""

    def __init__(self, directory=None):
        """
        :param directory: path to download directory; temporary dir if None
        """
        self.directory = directory

    @staticmethod
    def _download_file_from_url(url, directory=None):
        """
        Download file from given URL and save it in given directory

        :param url: URL of file
        :param directory: path to download directory
        :return: path to downloaded file
        """
        # Files are saved in temporary folder if `directory` isn't specified
        if not directory:
            return urlretrieve(url)[0]
        else:
            # Get the filename from URL
            css_filename = os.path.join(directory, url.split('/')[-1])
            return urlretrieve(url, filename=css_filename)[0]

    @staticmethod
    def _get_latest_tag_from_github(repo_api_url):
        """Get latest icon font tag via GitHub API"""
        url = '/'.join([repo_api_url, 'tags'])
        r = requests.get(url)
        latest = r.json()[0]

        return latest['name']

    @abstractmethod
    def get_latest_version_number(self):
        """Get latest icon font version number"""

    def download_css(self, directory):
        """Downloads icon font CSS file and returns its path"""
        return self._download_file_from_url(self.css_url, directory)

    def download_ttf(self, directory):
        """Downloads icon font TTF file and returns its path"""
        return self._download_file_from_url(self.ttf_url, directory)

    def download_files(self):
        """Download CSS and TTF files"""
        self.css_path = self.download_css(self.directory)
        self.ttf_path = self.download_ttf(self.directory)


class FontAwesomeDownloader(IconFontDownloader):
    """
    Font Awesome icon font downloader
    Project page:
        https://fortawesome.github.io/Font-Awesome/
    """
    css_url = ('https://raw.githubusercontent.com/FortAwesome/'
               'Font-Awesome/master/css/font-awesome.css')
    ttf_url = ('https://raw.githubusercontent.com/FortAwesome/'
               'Font-Awesome/master/fonts/fontawesome-webfont.ttf')

    def get_latest_version_number(self):
        return self._get_latest_tag_from_github(
            'https://api.github.com/repos/FortAwesome/Font-Awesome'
        )


class OcticonsDownloader(IconFontDownloader):
    """
    Octicons icon font downloader
    Project page:
        https://octicons.github.com/
    """
    css_url = ('https://raw.githubusercontent.com/github/'
               'octicons/master/octicons/octicons.css')
    ttf_url = ('https://raw.githubusercontent.com/github/'
               'octicons/master/octicons/octicons.ttf')

    def get_latest_version_number(self):
        return self._get_latest_tag_from_github(
            'https://api.github.com/repos/github/octicons'
        )


# List of implemented icon font downloader classes
AVAILABLE_ICON_FONTS = {
    'font-awesome': {
        'name': 'Font Awesome',
        'downloader': FontAwesomeDownloader,
    },
    'octicons': {
        'name': 'Octicons',
        'downloader': OcticonsDownloader,
    },
}
