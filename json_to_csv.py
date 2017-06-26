"""
    Name:           json_to_csv.py
    Created:        23/6/2017
    Description:    Convert json annotations to csv tables.
"""
#==============================================
#                   Modules
#==============================================
import sys
import json
import pandas as pd
#==============================================
#                   Files
#==============================================


#==============================================
#                   Functions
#==============================================
def json_to_pandas(json_name, val_prop=0.1, verbose=1):
    """
    Convert json file to pandas.
    """

    # read json
    with open(json_name, 'r') as iOF:
        json_dict = json.loads(iOF.read())

    # get df
    df_anno = pd.DataFrame(json_dict["annotations"])
    df_image = pd.DataFrame(json_dict["images"])
    df = df_image.merge(df_anno, how='inner', left_on="id", right_on="image_id")["file_name", "image_id", "category_id"]

    # split into train/val
    train_dfs, val_dfs = [], []
    categories = set(df["category_id"])
    for cat in categories:
        df_cat = df[df["category_id"] == cat].sample(frac=1)
        split_id = int(len(df_cat.index)*val_prop)
        val_dfs.append(df_cat.iloc[:split_id])
        train_dfs.append(df_cat.iloc[split_id:])
    train_df = pd.concat(train_dfs, ignore_index=True)
    val_df = pd.concat(val_dfs, ignore_index=True)

    return train_df, val_df

#==============================================
#                   Main
#==============================================
if __name__ == '__main__':
    json_name = str(sys.argv[1])
    train_df, val_df = json_to_pandas(json_name)
    train_csv_name = '.'.join(json_name.split('.')[:-1])+'_train.csv'
    val_csv_name = '.'.join(json_name.split('.')[:-1])+'_val.csv'
    train_df.to_csv(train_csv_name, index=False, header=True)
    val_df.to_csv(val_csv_name, index=False, header=True)
