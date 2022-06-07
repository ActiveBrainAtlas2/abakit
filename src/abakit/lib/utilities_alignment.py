import os, sys
import numpy as np
import pandas as pd
from skimage import io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import pickle
import re
from abakit.lib.Controllers.SqlController import SqlController
from abakit.lib.FileLocationManager import FileLocationManager
import tifffile as tiff
from scipy.ndimage import affine_transform

def create_downsampled_transforms(animal, transforms, downsample):
    """
    Changes the dictionary of transforms to the correct resolution
    :param animal: prep_id of animal we are working on
    :param transforms: dictionary of filename:array of transforms
    :param transforms_resol:
    :param downsample; either true for thumbnails, false for full resolution images
    :return: corrected dictionary of filename: array  of transforms
    """

    if downsample:
        transforms_scale_factor = 1
    else:
        transforms_scale_factor = 32

    tf_mat_mult_factor = np.array([[1, 1, transforms_scale_factor], [1, 1, transforms_scale_factor]])

    transforms_to_anchor = {}
    for img_name, tf in transforms.items():
        transforms_to_anchor[img_name] = \
            convert_2d_transform_forms(np.reshape(tf, (3, 3))[:2] * tf_mat_mult_factor) 
    return transforms_to_anchor

def convert_2d_transform_forms(arr):
    return np.vstack([arr, [0, 0, 1]])

def transform_points(points, transform):
    a = np.hstack((points, np.ones((points.shape[0], 1))))
    b = transform.T[:, 0:2]
    c = np.matmul(a, b)
    return c

def clean_image(file_key):
    index, infile, outfile, T = file_key
    image = tiff.imread(infile)
    matrix = T[:2,:2]
    offset = T[:2,2]
    offset = np.flip(offset)
    image1 = affine_transform(image,matrix.T,offset)
    tiff.imsave(outfile,image1)
    del image,image1
    return

