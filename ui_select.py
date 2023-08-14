import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import os
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

import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import os

def adjust_contrast(img):
    # Convert the image to numpy array
    np_img = np.array(img)
    
    # Rescale the pixel values to 0-255 range
    np_img = 255 * (np_img - np_img.min()) / (np_img.max() - np_img.min())
    
    # Convert back to an image
    img = Image.fromarray(np.uint8(np_img))
    
    return img

class ImageViewer(tk.Tk):
    def __init__(self, image_files):
        super().__init__()

        self.images = [adjust_contrast(Image.open(img)) for img in image_files]
        self.current_image_index = 0
        self.label = tk.Label(self)
        self.label.pack(padx=20, pady=20)
        self.show_image(self.current_image_index)
        
        # # Bind the right arrow key to the next_image function
        # self.bind("<Right>", self.next_image)
        # # Bind the left arrow key to the prev_image function
        # self.bind("<Left>", self.prev_image)

        # Bind the 'p' key to the custom_action function
        self.bind("p", self.good_image)
        # Bind the 'q' key to the custom_action function
        self.bind("q", self.bad_image)
        # Bind the 'z' key to the custom_action function
        self.bind("z", self.last_image)

    def show_image(self, index):
        print(f'{index}/{len(self.images)}')
        image = self.images[index]

        photo = ImageTk.PhotoImage(image)
        self.label.config(image=photo)
        self.label.image = photo

    # def next_image(self, event):
    #     self.current_image_index += 1
    #     if self.current_image_index >= len(self.images):
    #         self.current_image_index = 0
    #     self.show_image(self.current_image_index)

    # def prev_image(self, event):
    #     self.current_image_index -= 1
    #     if self.current_image_index < 0:
    #         self.current_image_index = len(self.images) - 1
    #     self.show_image(self.current_image_index)

    def good_image(self, event):

        name = image_files[self.current_image_index].split('/')[-1]
        shutil.copy2(image_files[self.current_image_index], os.path.join('./infocus',name))
            
        self.current_image_index += 1
        if self.current_image_index >= len(self.images):
            self.current_image_index = 0
        self.show_image(self.current_image_index)

    def bad_image(self, event):
    
        name = image_files[self.current_image_index].split('/')[-1]
        shutil.copy2(image_files[self.current_image_index], os.path.join('./outfocus',name))
        
        self.current_image_index += 1
        if self.current_image_index >= len(self.images):
            self.current_image_index = 0
        self.show_image(self.current_image_index)


    def last_image(self, event):
        name = image_files[self.current_image_index-1].split('/')[-1]
        file_path1 = os.path.join('./infocus',name)
        file_path2 = os.path.join('./outfocus',name)
        if os.path.exists(file_path1):
            os.remove(file_path1)
        if os.path.exists(file_path2):
            os.remove(file_path2)
        
        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = len(self.images) - 1
        self.show_image(self.current_image_index)    

if __name__ == "__main__":
    image_files = datapath_list = glob(os.path.join('../','*.tif'))
    viewer = ImageViewer(image_files)
    viewer.mainloop()
