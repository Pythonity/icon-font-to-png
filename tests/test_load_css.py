import tempfile
import unittest

from icon_font_to_png import load_css

class TestLoadCSS(unittest.TestCase):
    def create_css_file(self, contents):
        css_file = tempfile.NamedTemporaryFile()
        css_file.write(contents.encode('utf-8'))
        css_file.flush()
        return css_file

    def test_common_prefix(self):
        css_file = self.create_css_file(
            ".foo-bar:before { content: '\\f001' }\n"
            ".foo-xyzzy:before { content: '\\f002' }\n"
        )
        icons, prefix = load_css(css_file.name, strip_prefix=True)
        self.assertEqual(prefix, "foo-")

        css_file = self.create_css_file(
            ".foo:before { content: '\\f001' }\n"
            ".bar:before { content: '\\f002' }\n"
        )
        icons, prefix = load_css(css_file.name, strip_prefix=True)
        self.assertEqual(prefix, "")

if __name__ == '__main__':
    unittest.main
