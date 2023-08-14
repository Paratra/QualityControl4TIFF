from tifffile import imread
from scipy.ndimage import laplace
from glob import glob
from tqdm import tqdm
import os
import numpy as np
from pdb import set_trace as st
import matplotlib.pyplot as plt
import pandas as pd
import shutil

def main():

    datapath_list = glob(os.path.join('../','*.tif'))
    var_lap_list = []
    for each_path in tqdm(datapath_list):
        image = imread(each_path)
        lap = laplace(image)
        var_lap = np.var(lap)

        var_lap_list.append(var_lap)

    var_lap_df = pd.DataFrame(var_lap_list)
    # st()


    mean_var_lap = var_lap_df.quantile(0.25)[0]
    for each_path in tqdm(datapath_list):
        image = imread(each_path)
        lap = laplace(image)
        var_lap = np.var(lap)

        name = each_path.split('/')[-1]


        if var_lap >= mean_var_lap:
            # shutil.copy2(each_path, os.path.join('./infocus',name))
            pass
        else:
            shutil.copy2(each_path, os.path.join('./outfocus',name))

    print('done!')
    # st()






if __name__ == '__main__':
    main()