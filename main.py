# # LIBRARIES 
# # Image processing / computer vision
# import cv2
# from PIL import Image

# # Numerical calculations
# import numpy as np

# # Data handling
# import pandas as pd

# # Machine learning
# import tensorflow as tf
# from tensorflow import keras

# # Dataset splitting and model evaluation
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# # Image augmentation (for increasing training data)
# import albumentations as A

# # File and folder management
# import os
# from pathlib import Path

# # Visualization
# import matplotlib.pyplot as plt
# import seaborn as sns
# -----------------------------------------------------------------------

# img = (User inputs photo)
#Likelihood of bodypart:
    # Calculate body part likelihood of photo
    # Confirm w/ user (Y/N)
    # if Y:
        #run follow up
    # if N: 
        #ask user which body part
        #run follow up
#follow up:
    #Any other photos?
        #if Y:
             #run Area
        #if N:
            #move onto Intensity 

def user_input():
    image_path = []
    image = input ("Please insert an image of your affected area: ")
    image_path.append (image)
    print (image_path)
    return image_path
user_input()