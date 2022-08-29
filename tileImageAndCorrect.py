"""
Example: Stain normalize with Vahadane algorithm a list of H&E images.
Paper: "Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images", Vahadane et al, 2016.
"""

import os
import sys
from glob import glob

import numpy as np
from histocartography.preprocessing import VahadaneStainNormalizer
from histocartography.utils import download_example_data
from PIL import Image
from tqdm import tqdm
from typing import List
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# need to match the first name "files" for each uploaded file
@app.post("/normalize")
def normalize_images(files: List[UploadFile] = File(description="Images to process")):
    """
    Process the images in image path dir. In this dummy example,
    we use the first image as target for estimating normalization
    params.
    """
    # return {"filename": file.filename}
    for file in files:
        return {"filenames": [file.filename for file in files]}
    # 1. get image path
    # image_fnames = glob(os.path.join(image_path, '*.png'))

    # # 2. define stain normalizer. If no target target is provided,
    # # defaults ones are used. Note: Macenko normalization can be
    # # defined in a similar way.
    # target_image = image_fnames.pop(0)  # use the 1st image as target
    # normalizer = VahadaneStainNormalizer(target_path=target_image)

    # # 3. normalize all the images
    # for sing_image in tqdm(image_fnames):

    #     # a. load image
    #     _, image_name = os.path.split(sing_image)
    #     image = np.array(Image.open(sing_image))

    #     imageData = np.array_split(image, 8, axis=1)
    #     # b. apply Vahadane stain normalization
    #     for count, tiledImage in enumerate(imageData):
    #         norm_image = normalizer.process(tiledImage)

    #         # c. save the normalized image
    #         norm_image = Image.fromarray(np.uint8(norm_image))
    #         norm_image.save(
    #             os.path.join(
    #                 image_path,
    #                 'normalized_images',
    #                 f'{count}_{image_name}'))

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":

    path = sys.argv[1]
    
    # 2. create output directory
    os.makedirs(os.path.join(path, 'normalized_images'), exist_ok=True)

    # 3. normalize images
    normalize_images(path)
