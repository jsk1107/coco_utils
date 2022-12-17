import pycocotools
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import numpy as np


PATH = "/home/ubuntu/data/annotations/instances_val2017.json"
IMAGE_PATH = "/home/ubuntu/data/val2017/000000579900.jpg"

coco = COCO(PATH)

img = Image.open(IMAGE_PATH).convert('RGB')
annIds = coco.getAnnIds(imgIds=579900)
anns = coco.loadAnns(annIds)
plt.imshow(img)
coco.showAnns(anns=anns, draw_bbox=False)
plt.show()