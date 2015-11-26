from __future__ import unicode_literals
from six import with_metaclass, PY3

from abc import ABCMeta, abstractmethod
import os

if PY3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve


class IconFontDownloader(with_metaclass(ABCMeta)):
    """Abstract class for downloading icon font CSS and TTF files"""

    @property
    @abstractmethod
    def css_url(self):
        """Icon font CSS file URL"""
        pass

    @property
    @abstractmethod
    def ttf_url(self):
        """Icon font TTF file URL"""
        pass

    def __init__(self, directory=None):
        """
        :param directory: path to download directory
        """
        # Download CSS and TTF files
        self.css_path = self.download_css(directory)
        self.ttf_path = self.download_ttf(directory)

    @staticmethod
    def _download_file_from_url(url, directory):
        """
        Downloads file from given URL

        :param url: URL of file
        :param directory: path to download directory
        :return: path to downloaded file
        """
        # Files are saved in temporary folder if `directory` isn't specified
        if not directory:
            return urlretrieve(url)[0]
        else:
            # Get the filename from URL
            css_filename = os.path.join(directory,
                                        url.split('/')[-1])
            return urlretrieve(url, filename=css_filename)[0]

    def download_css(self, directory):
        """Downloads icon font CSS file and returns its path"""
        return self._download_file_from_url(self.css_url, directory)

    def download_ttf(self, directory):
        """Downloads icon font TTF file and returns its path"""
        return self._download_file_from_url(self.ttf_url, directory)


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


# List of implemented icon font download classes
AVAILABLE_ICONS = {'font-awesome': FontAwesomeDownloader,
                   'octicons': OcticonsDownloader}
