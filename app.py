import streamlit as st
import numpy as np
import tf_keras as keras
from PIL import Image, ImageOps
import statistics
import pandas as pdc
st.title ("SCORAD AI Prediction")

st.caption ("DISCLAIMER: This AI should not be used for official diagnostics")
st.markdown ("To get started, please upload images of affected skin area(s).")

class FixedDepthwiseConv2D(keras.layers.DepthwiseConv2D):
    def __init__(self, *args, **kwargs):
        kwargs.pop("groups", None)
        super().__init__(*args, **kwargs) 

# area calculator --------------------------------------------------------------------------------
image_parts = []
image_scan = []
total_area = []

def slider():
    sleep = st.slider("Rate your overall sleepiness", 1, 10, 0, key = "sleep_slider")

    itchiness = st.slider("Rate your overall itchiness", 1, 10, 0, key = "itch_slider")
    
    C_total = sleep + itchiness

    return C_total

def process_img(uploaded_file):
    # Open the new image
    image = Image.open(uploaded_file).convert("RGB")

    # Resize and crop the image to 224 x 224
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # Convert the image into a NumPy array
    image_array = np.asarray(image)

    # Normalize pixel values from 0–255 to -1–1
    normalized_image = (image_array.astype(np.float32) / 127.5) - 1

    return normalized_image

# def bdy_part(): #step 3
   

#     for i, _ in enumerate(image_parts, start=1):
C_total = slider()
def final (A_total, B_total):
       
        score = A_total/5 + 7*(B_total)/2 + C_total
        st.write ("Your SCORAD: ", score)
        if score <= 25:
            st.badge("None - Mild Status", color="green")
        elif 26<=score<=50:
            st.badge("Moderate Status", color="orange")
        elif score > 50:
            st.badge("Severe Status", color="red")
        
def user_input(): #step 1
    image = st.file_uploader( 
        "Upload data", 
        accept_multiple_files=True, 
        type=["jpg","jpeg","png"]
        )
   
    body_parts = (
            "Head/Neck",
            "Upper limbs",
            "Lower limbs",
            "Anterior Trunk",
            "Back",
            "Genitals"
        )
    
    if image:
        
        
        image_parts.clear()  # prevent duplicates when Streamlit reruns
        for i, uploaded_file in enumerate(image, start=1):
            image_parts.append(uploaded_file)
            st.image(
                uploaded_file,
                caption="Uploaded image"
            )
        
            selected = st.selectbox(
                f"User upload {uploaded_file.name}: Select body part",
                body_parts,
                key=f"body_part_{i}"
            )

    
        #t.button("Submit", type="primary", disabled = False)
            
                    
            
    
    return image_parts
    
user_input()

#st.button("Submit", type="primary", disabled = False)

A_total = sum (total_area)

# ----------------------------------------------------------

model_paths = ["dryness.h5","oozing_crusting.h5", "redness.h5","scratch_marks.h5","skin_thickening.h5","swelling.h5"]
labels_path = ["drynesslabels.txt","oozing_crustinglabels.txt","rednesslabels.txt","scratch_marks.txt","skin_thickening.txt","swelling.txt"]
factors=[]
if st.button("Submit", type="primary"):
   
    for ind,uploaded_file in enumerate(image_parts):
        
        st.write ("File: ", uploaded_file) 
        st.write ("AI Processing...")
        data = np.ndarray(
            shape=(1, 224, 224, 3),
            dtype=np.float32
        )

        normalized_image = process_img(uploaded_file)

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
            st.divider()
            
            category_title = model_paths[i].replace(".h5", "").replace("_", " ").upper()
            st.caption(f"{category_title} CLASSIFICATION")

            if class_name == "3 Severity (3)":
                st.caption("Severity: :red[Severe (3)]")
            elif class_name == "2 Severity (2)":
                st.caption("Severity: :orange[Moderate (2)]")
            elif class_name == "1 Severity (1)":
                st.caption("Severity: :green[Mild (1)]")
            else:
                st.caption("Severity: :gray[No Severity (1)]")
            # else:
            #     st.caption("Severity: None")
            st.caption(f"Confidence: {confidence * 100:.2f}%")
B_total = statistics.mode(factors) if factors else 0 
final(A_total, B_total)
        #for i, _ in enumerate(image_parts, start=1):
        # Load the model


    # Step D: Call final() ONCE at the very end




    # Final results 



    






