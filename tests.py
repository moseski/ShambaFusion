# import os
# import numpy as np
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image

# class DiseasePredictor:
#     def __init__(self, image_path):
#         self.image_path = image_path

#     def predict_disease(self):
#         model_path = 'model.weights.h5'  # Adjust if necessary
#         model = load_model(model_path)

#         img = image.load_img(self.image_path, target_size=(224, 224))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.0

#         predictions = model.predict(img_array)
#         predicted_class = np.argmax(predictions, axis=1)[0]

#         class_labels = [
#             'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Tomato_Bacterial_spot',
#             'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
#             'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
#             'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
#             'Tomato_healthy'
#         ]

#         disease_name = class_labels[predicted_class]
#         return disease_name

# # Example usage
# predictor = DiseasePredictor('/home/dominic/Shamba/PlantVillage/Tomato_Early_blight/0b494c44-8cd0-4491-bdfd-8a354209c3ae___RS_Erly.B 9561.JPG')  # Provide the path to an image file
# print("Predicted Disease:", predictor.predict_disease())
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import numpy as np

# Load the model
model_path = '/home/dominic/Shamba/disease_detection_model.keras'
model = load_model(model_path)

# Test prediction

img = load_img('/home/dominic/Downloads/potato-blight.jpg', target_size=(224, 224))  # Replace with your image path
img_array = img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0

predictions = model.predict(img_array)
predicted_class = np.argmax(predictions, axis=1)[0]

class_labels = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Tomato_Bacterial_spot',
    'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato_healthy'
]

disease_name = class_labels[predicted_class]
print("Predicted Disease:", disease_name)