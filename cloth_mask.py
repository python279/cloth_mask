#title Upload images from your computer
#markdown Description of parameters
#markdown - `SHOW_FULLSIZE`  - Shows image in full size (may take a long time to load)
#markdown - `PREPROCESSING_METHOD`  - Preprocessing method
#markdown - `SEGMENTATION_NETWORK`  - Segmentation network. Use `u2net` for hairs-like objects and `tracer_b7` for objects
#markdown - `POSTPROCESSING_METHOD`  - Postprocessing method
#markdown - `SEGMENTATION_MASK_SIZE` - Segmentation mask size. Use 640 for Tracer B7 and 320 for U2Net
#markdown - `TRIMAP_DILATION`  - The size of the offset radius from the object mask in pixels when forming an unknown area
#markdown - `TRIMAP_EROSION`  - The number of iterations of erosion that the object's mask will be subjected to before forming an unknown area

import os
from typing import List
import numpy as np
from PIL import Image, ImageOps
import torch
from carvekit.api.high import HiInterface
from carvekit.web.schemas.config import MLConfig
from carvekit.web.utils.init_utils import init_interface

SHOW_FULLSIZE = False #param {type:"boolean"}
PREPROCESSING_METHOD = "none" #param ["stub", "none"]
SEGMENTATION_NETWORK = "tracer_b7" #param ["u2net", "deeplabv3", "basnet", "tracer_b7"]
POSTPROCESSING_METHOD = "fba" #param ["fba", "none"]
SEGMENTATION_MASK_SIZE = 640 #param ["640", "320"] {type:"raw", allow-input: true}
TRIMAP_DILATION = 30 #param {type:"integer"}
TRIMAP_EROSION = 5 #param {type:"integer"}
DEVICE = 'cpu' # 'cuda'


class ClothMask(object):
    def __init__(self):
        self.interface = HiInterface(object_type="hairs-like",  # Can be "object" or "hairs-like".
                                     batch_size_seg=5,
                                     batch_size_matting=1,
                                     device='cuda' if torch.cuda.is_available() else 'cpu',
                                     seg_mask_size=320,  # Use 640 for Tracer B7 and 320 for U2Net
                                     matting_mask_size=2048,
                                     trimap_prob_threshold=231,
                                     trimap_dilation=1,
                                     trimap_erosion_iters=5,
                                     fp16=False)

    def __call__(self, imgs: List[Image.Image]) -> List[Image.Image]:
        parsed_images = []
        images = self.interface(imgs)
        for i, im in enumerate(images):
            img = np.array(im)
            img = img[..., :3]  # no transparency
            mask = np.any(img != [130, 130, 130], axis=-1)  # 判断非黑色像素
            img[mask] = [255, 255, 255]  # 将非黑色像素设置为白色
            img[~mask] = [0, 0, 0]  # 将黑色像素设置为黑色
            im = Image.fromarray(np.uint8(img))
            parsed_images.append(im)
        return parsed_images
