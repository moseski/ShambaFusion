from django.test import TestCase
from .models import Disease
from django.core.files.uploadedfile import SimpleUploadedFile
import os

# Create your tests here.
class DiseaseModelTest(TestCase):
    def setUp(self):
        with open('/home/dominic/Shamba/plantvillage_val/Tomato_Early_blight/0ba3d536-8732-4ea1-b3e1-a1be86e5dc6a___RS_Erly.B 9499.JPG', 'rb') as img_file:
            self.test_image = SimpleUploadedFile(
                name='test_image.jpg',
                content=img_file.read(),
                content_type='image/jpeg'
            )

        self.disease_instance = Disease.objects.create(
            # crop_type='tomatoes',
            symptoms="Sample symptoms",
            treatment="Sample treatment",
            image=self.test_image,
            additional_info="Sample info"
        )

    def test_predict_disease(self):
        predicted_disease = self.disease_instance.predict_disease()
        self.assertIsNotNone(predicted_disease)
        print("Predicted Disease:", predicted_disease)

# class DiseaseModelTest(TestCase):
#     def setUp(self):
#         with open('/home/dominic/Shamba/plantvillage_val/Tomato_Early_blight/0ba3d536-8732-4ea1-b3e1-a1be86e5dc6a___RS_Erly.B 9499.JPG', 'rb') as img_file:
#             self.test_image = SimpleUploadedFile(
#                 name='.jpg',
#                 content=img_file.read(),
#                 content_type='image/jpeg'
#             )

#     def test_disease_save_and_prediction(self):
#         disease_instance = Disease.objects.create(
#             # crop_type='tomatoes',
#             symptoms="Sample symptoms",
#             treatment="Sample treatment",
#             image=self.test_image,
#         )

#         # Verify fields after save
#         self.assertIsNotNone(disease_instance.additional_info, "Additional info not saved.")
#         self.assertNotEqual(disease_instance.symptoms, "Sample symptoms", "Symptoms not translated.")
#         self.assertIn("Treatment", disease_instance.treatment, "Treatment translation not processed.")

#         print("Disease Prediction:", disease_instance.__str__())
#         print("Additional Info:", disease_instance.additional_info)
#         print("Translated Symptoms:", disease_instance.symptoms)
#         print("Translated Treatment:", disease_instance.treatment)
