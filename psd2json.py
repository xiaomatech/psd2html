from psd_tools import PSDImage
import psd_tools.user_api.psd_image
import json
import os
import pinyin

class ImportPSD(object):
    """ Will Parse a PSD and store its data """
    data = {'pages': []}
    imagePath = './'
    psd = None
    PSDFilePath = None

    @classmethod
    def __init__(self, PSDFilePath, imagePath):
        self.PSDFilePath = PSDFilePath
        self.imagePath = imagePath
        self.psd = PSDImage.load(PSDFilePath)
        self.headers = self.psd.header
        self.layers = self.psd.layers
        self.nb_layers = self.countLayers(layers=self.psd.layers)
        print "Layers to process: %d" % self.nb_layers

    @classmethod
    def countLayers(self, layers, layer_num=0):
        for sheet in layers:
            if isinstance(sheet, psd_tools.user_api.psd_image.Layer):
                layer_num += 1
            elif isinstance(sheet, psd_tools.user_api.psd_image.Group):
                if sheet.visible_global:
                    layer_num = self.countLayers(layers=sheet.layers,
                                                 layer_num=layer_num)
        return layer_num

    @classmethod
    def parse(self):
        self.data['pages'].append(self.browseSheets(sheets=self.psd.layers,
                                                    parentName="root"))

    @classmethod
    def browseSheets(self, sheets, parentName, page_num=1):
        array = {}
        for sheet in sheets:
            if isinstance(sheet, psd_tools.user_api.psd_image.Layer):
                print "Processing layer: %d" % self.nb_layers
                self.nb_layers -= 1
                """ this sheet is a layer, it may be an image or some text """
                if sheet.text_data is not None:
                    """ If it's a text """
                    dic = dict({'name': sheet.name,
                                'x': sheet.bbox.x1,
                                'y': sheet.bbox.y2,
                                'width': sheet.bbox.width,
                                'height': sheet.bbox.height,
                                'string': sheet.text_data.text,
                                'font': None})
                    if 'paragraphs' not in array:
                        array['paragraphs'] = []
                    array['paragraphs'].append(dic)
                else:
                    """ If it's an image """
                    psd_name = os.path.basename(self.PSDFilePath)[:-4]
                    imageName = 'images/' + psd_name + '_' + sheet.name + '_' + parentName + '.png'
                    imageName = pinyin.get(imageName, format="strip")
                    if sheet is not None and sheet.as_PIL() is not None:
                        sheet.as_PIL().save(self.imagePath + imageName)
                    else:
                        imageName = None
                    if 'images' not in array:
                        array['images'] = []
                    array['images'].append(imageName)
            elif isinstance(sheet, psd_tools.user_api.psd_image.Group):
                """ this sheet is a group and may contains many layers """
                if sheet.visible_global:
                    arr = self.browseSheets(sheets=sheet.layers,
                                            parentName=sheet.name,
                                            page_num=page_num + 1)
                    self.data['pages'].append(arr)
        return array

    @classmethod
    def toJson(self):
        """ Will convert the parsed data array into json """
        return json.dumps(self.data)


def run(psd_file, image_folder='./output/'):
    image_folder_res = image_folder + '/json/'
    if os.path.exists(image_folder_res) is False:
        os.makedirs(image_folder_res)
    image_folder_image = image_folder + '/images/'
    if os.path.exists(image_folder_image) is False:
        os.makedirs(image_folder_image)
    importedPSD = ImportPSD(PSDFilePath=psd_file, imagePath=image_folder)
    print importedPSD.headers
    print importedPSD.layers
    sys.exit()
    importedPSD.parse()
    jsonString = importedPSD.toJson()
    result_file = os.path.basename(psd_file)[:-4]
    with open(image_folder_res + result_file + '.json', 'w+') as fout:
        fout.writelines(jsonString)
    image_dict = json.loads(jsonString)
    for item in image_dict['pages']:
        images = item.get('images')
        if images is not None:
            for image_file in images:
                print image_file
        paragraphs = item.get('paragraphs')
        if paragraphs is not None:
            for paragraph in paragraphs:
                name = paragraph.get('name')
                height = paragraph.get('height')
                width = paragraph.get('width')
                y = paragraph.get('y')
                x = paragraph.get('x')
                font = paragraph.get('font')
                string = paragraph.get('string')


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print run(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        print run(sys.argv[1])
    else:
        print "usage: python %s example.psd './output/' " % sys.argv[0]
