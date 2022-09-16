"""
Example: Stain normalize with Vahadane algorithm a list of H&E images.
Paper: "Structure-Preserving Color Normalization and Sparse Stain Separation for Histological Images", Vahadane et al, 2016.
"""

import base64
from fileinput import filename
import io
import os
import sys
from glob import glob
from typing import List

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, Response
from histocartography.preprocessing import VahadaneStainNormalizer
from histocartography.utils import download_example_data
from PIL import Image
from tqdm import tqdm
import zipfile

app = FastAPI()

# need to match the first name "files" for each uploaded file
@app.post("/normalize")
async def normalize_images(files: List[UploadFile] = File(description="Images to process")):
    """
    Process the images in image path dir. In this dummy example,
    we use the first image as target for estimating normalization
    params.
    """
    normalize_images = {}
    for file in files:
        contents = await file.read()

        nparr = np.fromstring(contents, np.uint8)

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        img_dimensions = str(img.shape)
        return_imgs = processImage(img)
        
        normalize_images[file.filename] = return_imgs

    zipFile = zipFiles(normalize_images)

    resp = Response(zipFile.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': 'attachment;filename=normalizedAndSplitPictures.zip'
    })

    return resp

def zipFiles(fileDict):
    zip_filename = "normalized_images.zip"

    s = io.BytesIO()

    zf = zipfile.ZipFile(s, "w")

    for image in fileDict:
        for count, normalized_image in enumerate(fileDict[image]):
            zf.writestr(f"{count}_{image}", normalized_image)
    
    zf.close()

    return s

def processImage(image):
    normalizer = VahadaneStainNormalizer()
    splitImage = np.array_split(image, 8, axis=1)
    splitImages = []
    for count, tiledImage in enumerate(splitImage):
        norm_image = normalizer.process(tiledImage)
        _, encoded_img = cv2.imencode('.PNG', norm_image)
        splitImages.append(encoded_img)
    return splitImages

@app.get("/")
async def root():
    return {"message": "If you want to normalize the images, make sure to send your images to /normalize"}

# create a quick function for local testing and bacalhau
def main(filename):
    # load image
    image = cv2.imread(filename)
    basename = os.path.basename(filename)
    basename = os.path.splitext(basename)[0]
    # process image
    split_images = processImage(image)
    # iterate over the split images and save them
    for count, tiled_image in enumerate(split_images):
        decoded_image = cv2.imdecode(tiled_image, cv2.IMREAD_COLOR)
        cv2.imwrite('/outputs/' + basename + "_normalized_tile_" + str(count) + ".png", decoded_image)
    # print success message
    print("Images processes and saved to /outputs")


if __name__ == "__main__":

    path = sys.argv[1]
    
    # 2. create output directory
    # os.makedirs(os.path.join(path, 'normalized_images'), exist_ok=True)
    os.makedirs('/outputs', exist_ok=True)

    # 3. normalize images
    main(path)
