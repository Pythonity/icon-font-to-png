import tempfile

def create_css_file(contents):
    css_file = tempfile.NamedTemporaryFile()
    css_file.write(contents.encode('utf-8'))
    css_file.flush()
    return css_file
