import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
#-------- Severity models
import numpy as np
import tf_keras as keras
import tensorflow as tf
from PIL import Image, ImageOps
import statistics

class FixedDepthwiseConv2D(keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)
        super().__init__(*args, **kwargs) 

# area calculator --------------------------------------------------------------------------------
image_parts = []
image_scan = []
total_area = []

def process_img(img_path):
    # Open the new image
    image = Image.open(img_path).convert("RGB")

    # Resize and crop the image to 224 x 224
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # Convert the image into a NumPy array
    image_array = np.asarray(image)

    # Normalize pixel values from 0–255 to -1–1
    normalized_image = (image_array.astype(np.float32) / 127.5) - 1

    return normalized_image

def bdy_part(): #step 3
    image_scan.clear()  
    for i, _ in enumerate(image_parts, start=1):
        image_scan.append(f"Image {i}")
        print (f"Image {i}", ":")
        x = int(input ("What is the body part?\n1.Head and neck \n2.Upper limb \n3.Lower limbs \n4.Anterior trunk \n5.Back \n6.Genitals\n"))
        if x == 1:
            total_area.append(9)
        elif x == 2:
            total_area.append(9)
        elif x == 3:
            total_area.append(18)
        elif x == 4:
            total_area.append(18)
        elif x == 5:
            total_area.append(18)
        elif x == 6:
            total_area.append(1)
        else:
            print ("Try again")

def follow_up(): #step 2
    add_img = input ("Do you have any other affected areas? (Y/N)")
    if add_img == "Y":
        user_input()
    if add_img == "N":
       bdy_part()

def user_input(): #step 1
    image = input ("Please insert an image of your affected area: ")
    image_parts.append (image)
    follow_up()
    return image_parts
user_input()

A_total = sum (total_area)

# Severity calculator -------------------------------------------------------------------------
model_paths = ["dryness.h5","oozing_crusting.h5", "redness.h5","scratch_marks.h5","skin_thickening.h5","swelling.h5"]
labels_path = ["drynesslabels.txt","oozing_crustinglabels.txt","rednesslabels.txt","scratch_marks.txt","skin_thickening.txt","swelling.txt"]
factors=[]

for ind, img_path in enumerate(image_parts):
    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    normalized_image = process_img(img_path)

    # Put the image into the input array
    data[0] = normalized_image

    #print("Image:", "test_image.jpg")
    factors.append(0)

    for i in range(len(model_paths)):
    # Load the model
        model = keras.models.load_model(
            model_paths[i],
            compile=False
        )

        # Load the class names
        with open(labels_path[i], "r") as file:
            class_names = file.readlines()

        # Ask the model to make a prediction
        prediction = model.predict(data, verbose=0)

        # Find the class with the highest confidence
        class_index = np.argmax(prediction[0])
        class_name = class_names[class_index].strip()
        confidence = prediction[0][class_index]
        factors[ind] += class_index
        print("=" * 40)
        print ("Image", img_path)
        print(model_paths[i].strip(".h5").upper(), "CLASSIFICATION")
        print("=" * 40)
        
        print("Prediction:", class_name)
        print("Confidence:", f"{confidence * 100:.2f}%")
        #for i, _ in enumerate(image_parts, start=1):
        # Load the model

    

    
#get the average factor per image, choose the image closest to the average as rep

ave_fac = statistics.mode(factors)
B_total = ave_fac
print (B_total)
# Questions -------------------------------------------------------------------------------------
sleep = int(input ("Rate overall sleepiness on a scale of 1-10"))
itchiness = int(input ("Rate overall itchiness on a scale of 1-10"))
C_total = sleep + itchiness

# Final results 
score = A_total/5 + 7*(B_total)/2 + C_total
print ("This is your SCORAD score", score)
if score <= 25:
    print ("Mild status")
elif 26<=score<=50:
    print ("Moderate status")
elif score > 50:
    print ("Severe Status") 
    print ("Specialist visit recommend")

