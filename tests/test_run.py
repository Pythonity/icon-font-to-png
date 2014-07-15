import glob
import os
import sys
import shutil, tempfile
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import icon_font_to_png

class TestRun(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory when we're done
        shutil.rmtree(self.test_dir)

    def create_css_file(self, contents):
        css_file = tempfile.NamedTemporaryFile()
        css_file.write(contents.encode('utf-8'))
        css_file.flush()
        return css_file

    def test_usage(self):
        orig_stderr = sys.stderr
        sys.stderr = StringIO()

        self.assertRaises(SystemExit, icon_font_to_png.run, [])
        
        err = sys.stderr.getvalue().strip()
        self.assertRegexpMatches(err, '^usage: .*')
        
        sys.stderr = orig_stderr

    def test_list(self):
        css_file = self.create_css_file(
            ".foo-xyzzy:before { content: '\\f003' }\n"
            ".foo-baz:before { content: '\\f002' }\n"
            ".foo-bar:before { content: '\\f001' }\n"
        )

        orig_stdout = sys.stdout
        sys.stdout = StringIO()

        self.assertRaisesRegexp(SystemExit, '^0', 
            icon_font_to_png.run, ['foo.ttf', css_file.name, 'bar', '--list'])

        out = sys.stdout.getvalue()
        self.assertEqual(out,
            "bar\n"
            "baz\n"
            "xyzzy\n"
        )

        sys.stdout = StringIO()

        self.assertRaisesRegexp(SystemExit, '^0',
            icon_font_to_png.run, ['foo.ttf', css_file.name, 'bar', '--list',
                '--keep-prefix'])

        out = sys.stdout.getvalue()
        self.assertEqual(out,
            "foo-bar\n"
            "foo-baz\n"
            "foo-xyzzy\n"
        )

        sys.stdout = orig_stdout

    def test_icon(self):
        css_file = self.create_css_file(
            ".beer:before { content: '\\f069' }\n"
            ".squirrel:before { content: '\\f0b2' }\n"
            ".zap:before { content: '\\26A1' }\n"
        )

        this_dir = os.getcwd()

        os.chdir(self.test_dir)

        # Export one icon
        icon_font_to_png.run([
            os.path.join(this_dir, 'tests/run/icon/octicons.ttf'),
            css_file.name,
            'beer'
        ]);
        
        self.assertTrue(os.path.isfile('beer.png'))

        for f in glob.glob(os.path.join('*.png')):
            os.remove(f)

        # Export two icons
        icon_font_to_png.run([
            os.path.join(this_dir, 'tests/run/icon/octicons.ttf'),
            css_file.name,
            'beer', 'squirrel'
        ]);
        
        self.assertTrue(os.path.isfile('beer.png'))
        self.assertTrue(os.path.isfile('squirrel.png'))

        for f in glob.glob(os.path.join('*.png')):
            os.remove(f)

        # Export all icons
        icon_font_to_png.run([
            os.path.join(this_dir, 'tests/run/icon/octicons.ttf'),
            css_file.name,
            'ALL'
        ]);
        
        self.assertTrue(os.path.isfile('beer.png'))
        self.assertTrue(os.path.isfile('squirrel.png'))
        self.assertTrue(os.path.isfile('zap.png'))

        for f in glob.glob(os.path.join('*.png')):
            os.remove(f)

        os.chdir(this_dir)

    def test_filename(self):
        css_file = self.create_css_file(
            ".beer:before { content: '\\f069' }\n"
            ".squirrel:before { content: '\\f0b2' }\n"
            ".zap:before { content: '\\26A1' }\n"
        )

        this_dir = os.getcwd()

        os.chdir(self.test_dir)

        # Export one icon
        icon_font_to_png.run([
            os.path.join(this_dir, 'tests/run/icon/octicons.ttf'),
            css_file.name,
            'beer',
            '--filename', 'beverage.png'
        ]);
        
        self.assertTrue(os.path.isfile('beverage.png'))

        for f in glob.glob(os.path.join('*.png')):
            os.remove(f)

        # Export multiple icons
        icon_font_to_png.run([
            os.path.join(this_dir, 'tests/run/icon/octicons.ttf'),
            css_file.name,
            'beer', 'squirrel',
            '--filename', 'foo'
        ]);
        
        self.assertTrue(os.path.isfile('foobeer.png'))
        self.assertTrue(os.path.isfile('foosquirrel.png'))

        for f in glob.glob(os.path.join('*.png')):
            os.remove(f)

        os.chdir(this_dir)

if __name__ == '__main__':
    unittest.main
