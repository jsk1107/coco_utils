# coco_utils
When pre-processing and post-processing image, sometimes you need to add, adjust, or remove categories in the coco json file. Also, train, val, and test should be separated from one json file. coco_utils is a module that provides these functions.

Using this, you will be able to process coco json files easily.

## Install
You only need to install the pycocotools.
```Shell
$ git clone https://github.com/jsk1107/coco_utils.git
$ pip install pycocotools
```

## Usage

```python
from coco import CocoUtils

PATH = '{your_coco_json_file}'
coco_util = CocoUtils(PATH)
```


```python
import json
from coco import CocoUtils

with open(PATH, 'r') as f:
    coco = json.load(f)
coco_util = CocoUtils(coco)
```

- Even if you have already opened a COCO Json file, you can create a class instance.
- Of course, all functions provided by pycocotools are also available.

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

