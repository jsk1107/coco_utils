import json
from pycocotools.coco import COCO
import time

class CocoUtils(COCO):
    def __init__(self, annotation_file=None):
        super().__init__()

        tic = time.time()
        if isinstance(annotation_file, str):
            print('loading annotations into memory...')
            with open(annotation_file, 'r') as f:
                dataset = json.load(f)
        elif isinstance(annotation_file, dict):
            dataset = annotation_file
            print('Indexing annotations into json ...')
        assert type(dataset) == dict, f'annotation file format {type(dataset)} not supported'
        print(f'Done (t={time.time() - tic:.2f}s)')

        self.dataset = dataset
        self.createIndex()

    def del_category(self):
        pass

    def adj_category(self):
        pass

    def add_category(self):
        pass

    def split_train_val_test(self):
        pass

    def transform_pascal2coco(self):
        pass

    def transform_coco2pascal(self):
        pass

if __name__ == '__main__':
    PATH = "/home/ubuntu/data/annotations/instances_val2017.json"
    IMAGE_PATH = "/home/ubuntu/data/val2017/000000579900.jpg"

    with open(PATH, 'r') as f:
        dataset = json.load(f)


    coco = CocoUtils(dataset)
    print(isinstance(coco, CocoUtils))
    # coco = COCO(PATH)
    #
    # img = Image.open(IMAGE_PATH).convert('RGB')
    # annIds = coco.getAnnIds(imgIds=579900)
    # anns = coco.loadAnns(annIds)
    # plt.imshow(img)
    # coco.showAnns(anns=anns, draw_bbox=False)
    # plt.show()
