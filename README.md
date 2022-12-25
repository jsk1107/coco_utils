# coco_utils

You can easily modify category and annotation information of coco data format. Also, it can be separated into train, val, and test from one coco data format.


## Install
You only need to install the pycocotools.
```Shell
pip install pycocotools
```

## Usage

```python
from coco import CocoUtils

PATH = '{your_coco_json_file}'
coco_util = CocoUtils(PATH)
```

If you have already opened the COCO Json file and put it in memory, you can also instantiate it.

```python
import json
from coco import CocoUtils

with open(PATH, 'r') as f:
    coco = json.load(f)
coco_util = CocoUtils(coco)
```

### delete category
```python
coco_util.del_category("person")
# or
coco_util.del_category(["person", "dog", "book", ...])
```
-  Enter an argument of type `str` or `list`.
-  All information of categories and annotations is lost.
-  If it is an wrong category name, nothing is deleted.

### adjust category
```python
coco_util.adj_category(bf_catNms="person", af_catNms="people")
# or
coco_util.del_category(bf_catNms=["person", "dog"], af_catNms=["people", "fox"]) # ok
coco_util.del_category(bf_catNms=["people", "dogs"], af_catNms=["human", "fox"]) # error. because people dose not exist.
```

- Enter an argument of type `str` or `list`.
- Match ordered pairs of arguments.
- If you adjust a category(`bf_catNms`) that does not exist, an error occurs.
- About `category_id` of `annotations`, category_id corresponding to `bf_Nms` is changed to category_id corresponding to `af_Nms`.

### add category
```python
coco_util.add_category('hero')
# or
coco_util.add_category(['hero', 'iron man'])
```
- Enter an argument of type `str` or `list`.
- If you enter a category that already exists, an error occurs.
- Only added to `categories`. annotation information cannot be added.

### split train/val/test

```python
coco_util.split_train_val_test(val_ratio=.2, test_ratio=.1, save_dir='{your_save_dir}', set_seed=1)
```

- If test_ratio is not none, two json files `instance_default_train.json` and `instance_default_val.json` are created. 
- If you set the seed, you can get the same split result.

