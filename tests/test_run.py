import sys
import tempfile
import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import icon_font_to_png

class TestRun(unittest.TestCase):
    def create_css_file(self, contents):
        css_file = tempfile.NamedTemporaryFile()
        css_file.write(contents.encode('utf-8'))
        css_file.flush()
        return css_file

    def test_usage(self):
        orig_stderr = sys.stderr
        sys.stderr = StringIO()

        self.assertRaises(SystemExit, icon_font_to_png.run,
            ['icon_font_to_png.py'])
        
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

if __name__ == '__main__':
    unittest.main
