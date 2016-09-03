from line import line
from cStringIO import StringIO


class paragraph(object):

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

    def __init__(self, xml_paragraph):
        (left, top, self._width,
         self._height) = xml_paragraph.get('bbox').split(',')
        self._width = int(float(self._width))
        self._height = int(float(self._height))
        self._x = int(float(left)) - self._width
        self._y = int(float(top)) - self._height
        #
        xml = xml_paragraph.find_all('textline')
        self._lines = []
        for l in xml:
            self._lines.append(line(l))
        #
        self._font = self._lines[0].font if len(self._lines) > 0 else None
        self._size = self._lines[0].size if len(self._lines) > 0 else None

    def toDict(self):
        dico = dict({'font': self._font,
                     'size': self._size,
                     'x': self._x,
                     'y': self._y,
                     'width': self._width,
                     'height': self._height})
        string = StringIO()
        count = 0
        for l in self._lines:
            if count != 0:
                string.write("\n")
            string.write(str(l))
            count = 1
        dico.update({'string': string.getvalue()})
        return dico

    def __str__(self):
        string = StringIO()
        count = 0
        for l in self._lines:
            if count != 0:
                string.write("\n")
            string.write(str(l))
            count = 1
        return string.getvalue()
