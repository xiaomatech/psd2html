from cStringIO import StringIO
from char import char


class line(object):

    _width = 0
    _height = 0
    _x = 0
    _y = 0
    _font = None
    _lines = []

    @property
    def font(self):
        return self._font

    @property
    def size(self):
        return self._size

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __init__(self, xml_line):
        (left, top, self._width,
         self._height) = xml_line.get('bbox').split(',')
        self._width = int(float(self._width))
        self._height = int(float(self._height))
        self._x = int(float(left)) - self._width
        self._y = int(float(top)) - self._height
        #
        xml_string = xml_line.find_all('text')
        self._chars = []
        for c in xml_string:
            self._chars.append(char(c))
        #
        self._font = self._chars[0].font if len(self._chars) > 0 else None
        self._size = self._chars[0].size if len(self._chars) > 0 else None

    _italic_on = False

    def handle_italic(self, c, string):
        if self._italic_on is False and c.isItalic() is True:
            string.write('<i>')
            self._italic_on = True
        if self._italic_on is True and c.isItalic() is False:
            string.write('</i>')
            self._italic_on = False

    _bold_on = False

    def handle_bold(self, c, string):
        if self._bold_on is False and c.isBold() is True:
            string.write('<b>')
            self._bold_on = True
        if self._bold_on is True and c.isBold() is False:
            string.write('</b>')
            self._bold_on = False

    def __str__(self):
        string = StringIO()
        for c in self._chars:
            self.handle_italic(c, string)
            self.handle_bold(c, string)
            string.write(str(c))
        return string.getvalue()
