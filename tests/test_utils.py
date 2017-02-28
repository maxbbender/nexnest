import nexnest.application
from nexnest.utils.file import allowed_file


def testAllowedFile():
    return allowed_file('img.jpg') == True
