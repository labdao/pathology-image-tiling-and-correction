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
        
        normalize_images = {file.filename : return_imgs}
        #return {"normalized" : img[0]}
        # headers = {'Content-Disposition': 'inline; filename="test.png"'}
        # return Response(return_imgs[0], headers=headers, media_type='image/png')
        # return {"files": return_imgs}
        # return {filename: file.filename}

        # return {"filenames": [file.filename for file in files]}
    
    zipFile = zipFiles(normalize_images)

    resp = Response(zipFile.getvalue(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename=yee.zip'
    })

    return resp


    # headers = {'Content-Disposition': 'inline', 'filename' : "test.png"}
    # print(return_imgs[1])
    # return Response(return_imgs[1].tobytes(), headers=headers, media_type='image/png')

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

        # c. save the normalized image
        # norm_image
        # norm_image = Image.fromarray(np.uint8(norm_image))
        # print(norm_image)
        _, encoded_img = cv2.imencode('.PNG', norm_image)

    # encoded_img = base64.b64encode(encoded_img)
        splitImages.append(encoded_img)
    
    return splitImages

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
