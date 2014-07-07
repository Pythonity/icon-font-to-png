import atexit, shutil, tempfile
from os import path
import unittest
from PIL import Image, ImageChops

from icon_font_to_png import load_css, export_icon

class TestExportIcon(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        # Remove it when we're done
        atexit.register(shutil.rmtree, self.test_dir)

    def png_equal(self, png_file1, png_file2):
        im1 = Image.open(png_file1)
        im2 = Image.open(png_file2)
        return ImageChops.difference(im1, im2).getbbox() is None

    def test_size(self):
        icons, prefix = load_css('tests/export_icon/size/test.css',
            strip_prefix=False)

        png_file = path.join(self.test_dir, 'squirrel.png')
        
        export_icon(icons=icons, icon='squirrel', size=16, filename=png_file,
            ttf_file='tests/export_icon/size/octicons.ttf', color='black',
            scale=1)
        im = Image.open(png_file)
        self.assertEqual(im.size, (16, 16))

        export_icon(icons=icons, icon='squirrel', size=100, filename=png_file,
            ttf_file='tests/export_icon/size/octicons.ttf', color='black',
            scale=1)
        im = Image.open(png_file)
        self.assertEqual(im.size, (100, 100))

if __name__ == '__main__':
    unittest.main
