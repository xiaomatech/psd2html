from paragraph import paragraph
from cStringIO import StringIO


class page(object):

    _paragraphs = []

    @property
    def paragraphs(self):
        return self._paragraphs

    def __init__(self, xml_page):
        xml = xml_page.find_all('textbox')
        self._paragraphs = []
        for p in xml:
            self._paragraphs.append(paragraph(p))

    def toDict(self):
        array = {'paragraphs': []}
        for p in self._paragraphs:
            array['paragraphs'].append(p.toDict())
        return array

    def __str__(self):
        string = StringIO()
        count = 0
        for p in self._paragraphs:
            if count != 0:
                string.write("\n\n")
            string.write(str(p))
            count = 1
        return string.getvalue()
