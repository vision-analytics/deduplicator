import hashlib
import time
import os
import shutil
import sys
from glob import glob
from tqdm import tqdm
from typing import List

import cv2
import fire
import numpy as np
from matplotlib import pyplot as plt

from helpers import calculate_md5_hash

def find_duplicates_md5(image_list: List, img_dir: str):
    """
    find duplicates by calculating md5 hashes.

    Args:
        image_list: List. list of images with absolute paths
        img_dir: str. root directory of images
    """

    find_occurrences = lambda s, lst: (i for i,e in enumerate(lst) if e == s)

    md5_list = [calculate_md5_hash(image_path) for image_path in tqdm(image_list)]

    duplicates = {}

    processed_items = []
    for ref_image_path, ref_md5 in tqdm(zip(image_list, md5_list)):

        if ref_image_path in processed_items:
            continue
        processed_items.append(ref_image_path)
        
        similar_image_inds = list(find_occurrences(ref_md5, md5_list))
    
        for sim_image_ind  in similar_image_inds:
            similar_image_path = image_list[sim_image_ind]
            
            if similar_image_path == ref_image_path or similar_image_path in processed_items:
                continue
            new_duplicates = duplicates.get(ref_image_path, [])
            new_duplicates.append(similar_image_path)
            duplicates[ref_image_path] = new_duplicates
            processed_items.append(similar_image_path)
    return duplicates



def run_vgg():
    pass

METHOD2FUNC = {
    "md5": find_duplicates_md5,
    "vgg": run_vgg
}
IMG_EXT = ['png', 'jpg', 'jpeg']

ACTION2FUNC = {
    "copy": shutil.copy,
    "move": shutil.move
}


def get_image_list(img_dir:str) -> List:
    files = []
    for ext in IMG_EXT:
        img_list = glob(f"{img_dir}/*.{ext}")
        if img_list:
            files.extend(img_list)
    return files

def main(method: str, img_dir: str, action: str = "copy") -> None:

    if method not in METHOD2FUNC:
        return f"method {method} is not supported."

    if action not in ACTION2FUNC:
        return f"action {action} is not supported."

    func2run = METHOD2FUNC[method]
    action2take = ACTION2FUNC[action]

    if img_dir[-1] == "/":
        img_dir = img_dir[:-1]
    staging_dir = img_dir+"_duplicates"
    print(f"DUPLICATES WILL BE {action2take} TO {staging_dir}")

    if os.path.exists(staging_dir):
        if not input("CAUTION: target directory exists. Are you sure? (y/n)") == "y":
            print("exit.")
            sys.exit()
    else:
        os.makedirs(staging_dir)


    image_list = get_image_list(img_dir)

    print(f"{len(image_list)} images found in {img_dir}")

    duplicates = func2run(image_list, img_dir)
    
    # move duplicates to staging dir
    counter = 0
    for ref_image_path, similar_image_paths in duplicates.items():
        file_name = os.path.basename(ref_image_path)
        new_path = os.path.join(staging_dir, file_name)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        shutil.copy(ref_image_path, f"{new_path}/ref_{file_name}")
        for similar_image_path in similar_image_paths:
            action2take(similar_image_path, new_path)
            counter+=1

    print(f"{counter} duplicates found for {len(duplicates)} unique reference images. ACTION: {action}. See images in {staging_dir}")

if __name__ == "__main__":
    fire.Fire(main)