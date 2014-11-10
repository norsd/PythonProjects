__author__ = 'Administrator'

import pyexpat as expat
class Element(object):
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.cdata = ''
        self.children = []
    def __getitem__(self, item):
        if type(item) == str:
            elems = self.getElements(item)
            if len(elems) == 1:
                return elems[0]
            else:
                return elems
        if type(item) == int:
            return self.children[item]

    def addChild(self, element):
        self.children.append(element)

    def getAttribute(self, key):
        return str(self.attributes.get(key)).strip()

    def getData(self):
        return self.cdata

    def getElements(self, name=''):
        if name:
            return [c for c in self.children if c.name == name]
        else:
            return list(self.children)

    Value = property(getData)

class Xml2Obj(object):
    def __init__(self):
        self.root = None
        self.nodeStack = [ ]

    def StartElement(self, name, attributes):
        'Expat start element event handler'
        element = Element(str(name).strip(), attributes)
        if self.nodeStack:
            parent = self.nodeStack[-1]
            parent.addChild(element)
        else:
            self.root = element
        self.nodeStack.append(element)

    def EndElement(self, name):
        'Expat end element event handler'
        self.nodeStack.pop()

    def CharacterData(self, data):
        'Expat character data event handler'
        if data.strip():
            #data = data.encode()
            element = self.nodeStack[-1]
            element.cdata += str(data).strip()

    def Parse(self, content):
        Parser = expat.ParserCreate()
        Parser.StartElementHandler = self.StartElement
        Parser.EndElementHandler = self.EndElement
        Parser.CharacterDataHandler = self.CharacterData
        #ParserStatus = Parser.Parse(open(filename).read(), 1)
        ParserStatus = Parser.Parse(content, 1)
        return self.root


parser = Xml2Obj()
root_element = parser.Parse(open('d:\\IF.xml').read())


