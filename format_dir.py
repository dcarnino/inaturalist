"""
    Name:           format_dir.py
    Created:        28/6/2017
    Description:    Format train_val directory into separate train and val.
"""
#==============================================
#                   Modules
#==============================================
import sys
import json
import pandas as pd
import shutil
import os
#==============================================
#                   Files
#==============================================


#==============================================
#                   Functions
#==============================================
def format_dir(train_val_dir="../data/inaturalist/",
               target_dir="../data/inaturalist/train_images/",
               name_csv="../data/inaturalise/train2017.csv",
               verbose=1):
    """
    Format dir into keras on-the-fly image generator format.
    """

    ### train and val dfs
    df = pd.read_csv(name_csv)

    ### loop over images
    for ix, (image_path, image_id, category_id) in df.iterrows():
        # get names
        tv_dir, super_cat_dir, cat_dir, image_name = image_path.split("/")
        ori_image_path = "%s%s"%(train_val_dir, image_path)
        new_image_dir = "%s%d/"%(target_dir, category_id)
        new_image_path = "%s%d_%s"%(new_image_dir, image_id, image_name)
        # create category dir
        if not os.path.exists(new_image_dir):
            os.makedirs(new_image_dir)
        # copy image
        shutil.copy(ori_image_path, new_image_path)



#==============================================
#                   Main
#==============================================
if __name__ == '__main__':
    format_dir(train_val_dir="../data/inaturalist/",
               target_dir="../data/inaturalist/train_images/",
               name_csv="../data/inaturalise/train2017.csv")
    format_dir(train_val_dir="../data/inaturalist/",
               target_dir="../data/inaturalist/val_images/",
               name_csv="../data/inaturalise/val2017.csv")
