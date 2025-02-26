# from django.db import models
# from tensorflow.keras.models import load_model
# from django.conf import settings
# from tensorflow.keras.preprocessing import image
# import numpy as np
# import requests
# import os
# class Disease(models.Model):
#     crop_type = models.CharField(max_length=30, choices=[('tomatoes', 'Tomatoes'), ('french beans', 'French beans')])
#     symptoms = models.TextField(blank=True, null=True)
#     treatment = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='diseases_images/')
#     additional_info = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"Disease Prediction for {self.crop_type}"

#     def predict_disease(self):
#         """Load the trained model and predict the disease based on the uploaded image."""
#         model_path = os.path.join(settings.BASE_DIR, '/home/dominic/Shamba/disease_detection_model.keras')
#         model = load_model(model_path)

#         img = image.load_img(self.image.path, target_size=(224, 224))
#         img_array = image.img_to_array(img)
#         img_array = np.expand_dims(img_array, axis=0)
#         img_array /= 255.0 
        
#         predictions = model.predict(img_array)
#         predicted_class = np.argmax(predictions, axis=1)[0]

#         # Map predicted class index to a disease label
#         class_labels = [
#             'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Tomato_Bacterial_spot',
#             'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
#             'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
#             'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
#             'Tomato_healthy'
#         ]
        
#         disease_name = class_labels[predicted_class]
#         return disease_name

#     def fetch_additional_info(self, disease_name):
#         """Fetch additional disease information (symptoms, treatment) using Bing API."""
#         subscription_key = settings.BING_SEARCH_V7_SUBSCRIPTION_KEY
#         search_url = "https://api.bing.microsoft.com/v7.0/search"
#         # search_url = settings.ENDPOINT + "/bing/v7.0/search"

        
#         headers = {"Ocp-Apim-Subscription-Key": subscription_key}
#         params = {"q": f"{disease_name} symptoms treatment", "textDecorations": True, "count": 3}
        
#         response = requests.get(search_url, headers=headers, params=params)
#         response.raise_for_status()
#         search_results = response.json()

#         # Extract info from search 
#         return search_results.get("webPages", {}).get("value", [])

#     def translate_to_swahili(self, text):
#         """Translate text to Swahili using Azure Translator API."""
#         translate_url = settings.TRANSLATOR_URL,
#         headers = {
#             'Ocp-Apim-Subscription-Key': settings.TRANSLATOR_API_KEY,
#             'Content-Type': 'application/json'
#         }
#         body = [{'text': text}]
        
#         response = requests.post(translate_url, headers=headers, json=body)
#         response.raise_for_status()
#         translated_text = response.json()[0]['translations'][0]['text']
#         return translated_text

#     def save(self, *args, **kwargs):
#         """Override the save method to integrate prediction, fetching additional info, and translation."""
#         if not self.pk:
#             disease_name = self.predict_disease()
#             additional_info = self.fetch_additional_info(disease_name)

#             if additional_info:
#                 snippet = additional_info[0].get('snippet', '')
#                 self.additional_info = self.translate_to_swahili(snippet)
                
#             self.symptoms = self.translate_to_swahili(self.symptoms or '')
#             self.treatment = self.translate_to_swahili(f"Treatment for {disease_name}")

#         super().save(*args, **kwargs)

from django.db import models
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import openai
import os
import requests
# from googletrans import Translator
from deep_translator import GoogleTranslator


class Disease(models.Model):
    CROP_CHOICES = [
        ('tomatoes', 'Tomatoes')
        # ('french beans', 'French beans')
    ]
    crop_type = models.CharField(max_length=30, choices=CROP_CHOICES)
    symptoms = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='diseases_images/')
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Disease Prediction for {self.crop_type}"

    def predict_disease(self):
        """Load the trained model and predict the disease based on the uploaded image."""
        model_path = os.path.join(settings.BASE_DIR, 'C:/Users/HP/Downloads/disease_detection/disease_detection_model.keras')
        model = load_model(model_path)

        img = image.load_img(self.image.path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)
        
        class_labels = [
            'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Tomato_Bacterial_spot',
            'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
            'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
            'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus', 
            'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato_healthy'
        ]
        # return class_labels[predicted_class]
        # print(predicted_class)
        if predicted_class < len(class_labels):
            disease_name = class_labels[predicted_class]
            print(f"Predicted Disease: {disease_name}")
            return disease_name
        else:
            print("Prediction out of range")
            return None


    def get_disease_info(self, disease_name):
        """Fetch detailed disease information using Azure OpenAI GPT."""
        prompt = (
            f"Provide detailed information about the disease '{disease_name}', including symptoms, "
            "causes, treatments, and recommended actions. Please translate the content into both English and Swahili."
        )
        
        openai.api_key = settings.AZURE_OPENAI_API_KEY
        openai.api_base = settings.AZURE_OPENAI_API_ENDPOINT
        openai.api_version = "2024-06-01-preview" 
        
        try:
            response = openai.Completion.create(
                model="gpt-4",
                # messages=[{"role": "user", "content": prompt}],
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            print(f"ShambaFusion Model response: {response}")
            # return response.choices[0].message['content'].strip()
            return response.choices[0].text.strip()
        except openai.OpenAIError as e:
            return f"Error fetching information: {e}"

    # def save(self, *args, **kwargs):
    #     """Override save to perform disease prediction and fetch additional information."""
    #     if not self.pk:
    #         disease_name = self.predict_disease()
    #         self.symptoms = self.get_disease_info(disease_name)
    #         self.treatment = f"Recommended treatment for {disease_name}"
        
    #     super().save(*args, **kwargs)
    # def translate_to_swahili(self, text):
    #     """Translate the given text to Swahili using Google Translator."""
    #     translator = Translator()
    #     try:
    #         translation = translator.translate(text, dest='sw')
    #         return translation.text
    #     except Exception as e:
    #         return f"Translation Error: {str(e)}"
    # @staticmethod
    def translate_to_swahili(self, text):
        """Translate the given text to Swahili using Google Translator."""
        try:
            # Use deep-translator's GoogleTranslator for translation
            translation = GoogleTranslator(source='auto', target='sw').translate(text)
            return translation
        except Exception as e:
            return f"Translation Error: {str(e)}"
        
    def save(self, *args, **kwargs):
        """Override the save method to integrate prediction, fetching additional info, and translation."""
        # Ensure the image is saved before accessing its path
        if not self.pk:
            super().save(*args, **kwargs)
        
        # Check if image exists after saving
        if self.image and hasattr(self.image, 'path'):
            disease_name = self.predict_disease()
            additional_info = self.get_disease_info(disease_name)
            
            print(f"Additional Info: {additional_info}")


            if additional_info:
                # snippet = additional_info[:5].find('snippet', '')
                snippet = additional_info[:5] if isinstance(additional_info, str) else ''

                self.additional_info = self.translate_to_swahili(snippet)
            
            self.symptoms = self.translate_to_swahili(self.symptoms or '')
            self.treatment = self.translate_to_swahili(f"Treatment for {disease_name}")

        # Save again to store the additional data
        super().save(*args, **kwargs)

