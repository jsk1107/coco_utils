#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Original author: jsk1107

import json
import time
import random
import os
from pycocotools.coco import COCO

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

    def del_category(self, catNms=[], catIds=[]):
        st = time.time()
        catNms = catNms if isinstance(catNms, list) else [catNms]
        catIds = catIds if self._isArrayLike(catIds) else [catIds]

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

        print(f'the number of {cnt} is deleted from annotations')
        print(f're-indexing...')
        self.createIndex()
        print(f'Done (t={time.time() - st:.2f}s)')

    def adj_category(self, bf_catNms=[], af_catNms=[]):
        print('Adjust categories ... ')
        st = time.time()
        bf_catNms = bf_catNms if isinstance(bf_catNms, list) else [bf_catNms]
        af_catNms = af_catNms if isinstance(af_catNms, list) else [af_catNms]

        if len(bf_catNms) != len(af_catNms):
            raise Exception('the number of bf_catNms and af_catNms must be equal.')

        categories = self.dataset['categories']
        annotations = self.dataset['annotations']

        idx = 0
        while idx <= len(bf_catNms) - 1:

            bf_catNm, af_catNm = bf_catNms[idx], af_catNms[idx]
            bf_id = self.getCatIds(catNms=bf_catNm)
            if len(bf_id) == 0:
                raise Exception(f'{bf_catNm} does not exist')

            af_id = self.getCatIds(catNms=af_catNm)
            if len(af_id) == 0:
                for category in categories:
                    if category['name'] in bf_catNm:
                        category['name'] = af_catNm
                        print(f'{bf_catNm} change {af_catNm}.')
                        break
            else:
                cnt = 0
                for annotation in annotations:
                    if annotation['category_id'] not in bf_id:
                        continue
                    annotation['category_id'] = af_id[0]
                    cnt += 1
                print(f'"{bf_catNm}": annotation info of the number of {cnt} has been adjusted to "{af_catNm}"')

                cat_idx = 0
                while cat_idx <= len(categories) - 1:
                    if categories[cat_idx]['id'] in bf_id:
                        del categories[cat_idx]
                        continue
                    cat_idx += 1
            idx += 1

        print(f're-indexing...')
        self.createIndex()
        print(f'Done (t={time.time() - st:.2f}s)')

    def add_category(self, catNms=[]):
        st = time.time()
        catNms = catNms if isinstance(catNms, list) else [catNms]
        catIds = self.getCatIds(catNms=catNms)
        if len(catIds) != 0:
            raise Exception(f'{catNms} already exists.')

        categories = self.dataset['categories']
        last_id = categories[-1]['id']
        for catNm in catNms:
            last_id += 1
            categories.append({'id': last_id, 'supercategory': catNm, 'name': catNm})
        print(f're-indexing...')
        self.createIndex()
        print(f'Done (t={time.time() - st:.2f}s)')

    def sort_id(self):
        pass

    def split_train_val_test(self, val_ratio=.3, test_ratio=None, save_dir=None, set_seed=None):
        print('split data...')
        if set_seed is not None:
            random.seed(set_seed)

        st = time.time()
        all_imgIds = self.getImgIds()
        random.shuffle(all_imgIds)
        total_img = len(all_imgIds)
        train_ratio = 1 - val_ratio - test_ratio if test_ratio is not None else 1 - val_ratio
        train_idx = int(total_img * train_ratio)
        val_idx = int(total_img * val_ratio)
        train_imgIds = all_imgIds[:train_idx]

        if test_ratio is not None:
            val_imgIds = all_imgIds[train_idx:train_idx + val_idx]
            test_imgIds = all_imgIds[train_idx + val_idx:]
        else:
            val_imgIds = all_imgIds[train_idx:]
            test_imgIds = []

        train_dataset = self._create_coco_format(train_imgIds)
        val_dataset = self._create_coco_format(val_imgIds)
        test_dataset = self._create_coco_format(test_imgIds)

        if save_dir is None:
            save_dir = ''
        with open(os.path.join(save_dir, 'instatnce_default_train.json'), 'w') as f:
                json.dump(train_dataset, f, indent=2)
        with open(os.path.join(save_dir, 'instatnce_default_val.json'), 'w') as f:
                json.dump(val_dataset, f, indent=2)

        if len(test_dataset) != 0:
            with open(os.path.join(save_dir, 'instatnce_default_test.json'), 'w') as f:
                json.dump(test_dataset, f, indent=2)

        print(f'Done (t={time.time() - st:.2f}s)')


    def _create_coco_format(self, imgIds=[]):
        if len(imgIds) == 0:
            return {}

        imgs_info = self.loadImgs(imgIds)
        annotations_info = self.loadAnns(self.getAnnIds(imgIds))

        coco_format = {}
        coco_format['info'] = self.dataset['info']
        coco_format['licenses'] = self.dataset['licenses']
        coco_format['categories'] = self.dataset['categories']
        coco_format['images'] = imgs_info
        coco_format['annotations'] = annotations_info

        return coco_format

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

    # dog, 18, person, 20
    # clock, 85, teddy bear, 88
    # "supercategory": "vehicle",
    # "id": 5,
    # "name": "airplane"
    #
    # "supercategory": "vehicle",
    # "id": 6,
    # "name": "bus"

    coco = CocoUtils(dataset)
    coco.adj_category(["clock", "airplane"], ["teddy bear","book"])
    coco.del_category(["person", "dog", "asdf"])
    coco.add_category(["person", "asdf"])
    coco.split_train_val_test(val_ratio=.2, test_ratio=.1)
    # img = Image.open(IMAGE_PATH).convert('RGB')
    # annIds = coco.getAnnIds(imgIds=579900)
    # anns = coco.loadAnns(annIds)
    # plt.imshow(img)
    # coco.showAnns(anns=anns, draw_bbox=False)
    # plt.show()
