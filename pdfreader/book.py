from cStringIO import StringIO
from bs4 import BeautifulSoup
from page import page
import json


class book(object):

    _pages = []

    @property
    def pages(self):
        return self._pages

    def __init__(self, file):
        soup = BeautifulSoup(file)
        #
        xml = soup.find_all('page')
        self._pages = []
        for p in xml:
            self._pages.append(page(p))

    def toDict(self):
        array = {'pages': []}
        for p in self._pages:
            array['pages'].append(p.toDict())
        return array

    def toJson(self):
        return json.dumps(self.toDict())

    def __str__(self):
        string = StringIO()
        count = 0
        for p in self._pages:
            if count != 0:
                string.write('NEW PAGE')
            string.write(str(p))
            count = 1
        return string.getvalue()
