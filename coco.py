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

    def del_category(self, catIds=[], catNms=[]):
        catIds = catIds if self._isArrayLike(catIds) else [catIds]
        catNms = catNms if self._isArrayLike(catNms) else [catNms]

        if (len(catIds) == 0 and len(catNms) == 0) or (len(catIds) != 0 and len(catNms) != 0):
            raise Exception('Only one of catIds and catNms can be received as an argument.')

        categories = self.dataset['categories']
        annotations = self.dataset['annotations']

        if len(catIds) == 0 and len(catNms) != 0:
            catIds = self.getCatIds(catNms=catNms)

        cnt = 0
        # del category in categories
        idx = 0
        while idx <= len(categories) - 1:
            if categories[idx]['id'] in catIds:
                del categories[idx]
                continue
            idx += 1
        # del annotation in annotations
        idx = 0
        while idx <= len(annotations) - 1:
            if annotations[idx]['category_id'] in catIds:
                del annotations[idx]
                cnt += 1
                continue
            idx += 1

        print(f'{cnt} is deleted from annotations')
        print(f're-indexing...')
        self.createIndex()

    def adj_category(self):
        pass

    def add_category(self):
        pass

    def sort_id(self):
        pass

    def split_train_val_test(self):
        pass

    def transform_pascal2coco(self):
        pass

    def transform_coco2pascal(self):
        pass

    def _isArrayLike(self, obj):
        return hasattr(obj, '__iter__') and hasattr(obj, '__len__')

if __name__ == '__main__':
    PATH = "/home/ubuntu/data/annotations/instances_val2017.json"
    IMAGE_PATH = "/home/ubuntu/data/val2017/000000579900.jpg"

    with open(PATH, 'r') as f:
        dataset = json.load(f)

    # dog, 18
    coco = CocoUtils(dataset)
    print(coco.loadCats(20))
    coco.del_category(20)
    print(coco.loadCats(20))

    # coco.del_category(catIds=18)
    # print(isinstance(coco, CocoUtils))
    # coco = COCO(PATH)
    #
    # img = Image.open(IMAGE_PATH).convert('RGB')
    # annIds = coco.getAnnIds(imgIds=579900)
    # anns = coco.loadAnns(annIds)
    # plt.imshow(img)
    # coco.showAnns(anns=anns, draw_bbox=False)
    # plt.show()
