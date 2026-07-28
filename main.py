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

def upload_image():
    user_upload = input ("Upload you image here: ")
    #image = (user_upload)
    return upload_image()

def body_part_calc ():
   part = ("Leg") # (take code from main.py in CV (coding mind file))
   return body_part_calc()

def follow_up():
    x = input ("Do you have any other affected areas? (Y/N) ")
    if x == "Y":
        return 
    elif x == "N":
        return check_body_part()
    return follow_up()

def check_body_part (): 
    print ("The image you took contains", (part), "correct?")
    accuracy = input ("Y/N? ")
    if accuracy == "Y":
        return follow_up
    elif accuracy == "N":
        print ("What is the part?")
    else:
        print ("I don't understand")
    return check_body_part()