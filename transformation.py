
import os
import pandas as pd
from PIL import Image, ImageEnhance
import random
import csv
import numpy as np

def change_temperature(image, factor):
    img_array = np.array(image).astype(np.float32)

    red, green, blue = img_array[..., 0], img_array[..., 1], img_array[..., 2]

    if factor > 1.0:
        red *= factor
        blue /= factor
    else:
        red /= factor
        blue *= factor

    red = np.clip(red, 0, 255)
    blue = np.clip(blue, 0, 255)

    img_array[..., 0], img_array[..., 1], img_array[..., 2] = red, green, blue
    img_array = img_array.astype(np.uint8)
    return Image.fromarray(img_array)

def apply_transformations(image_path, transformations, reverse=False):
    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(transformations['brightness']) # 'brightness
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(transformations['saturation']) # 'color'
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(transformations['contrast']) # 'contrast'
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(transformations['sharpness']) # 'sharpness'
    image = change_temperature(image, transformations['temperature']) # 'temperature'
    return image

def apply_reverse_transformations(image_path, transformations : np.ndarray):
    transformations = transformations.tolist()
    print(transformations)
    transformations = {
        'image_path': image_path,
        'brightness': 1/transformations[0],
        'saturation': 1/transformations[1],
        'contrast': 1/transformations[2],
        'sharpness': 1/transformations[3],
        'temperature': 1/transformations[4]
    }
    return apply_transformations(image_path, transformations)

def apply_random_transformations(image_path):
    transformations = {}
    transformations['image_path'] = image_path
    transformations['brightness'] = random.uniform(0.5, 1.5)
    transformations['saturation'] = random.uniform(0.5, 1.5)
    transformations['contrast'] = random.uniform(0.5, 1.5)
    transformations['sharpness'] = random.uniform(0.5, 1.5)
    transformations['temperature'] = random.uniform(0.5, 1.5)

    return apply_transformations(image_path, transformations), transformations