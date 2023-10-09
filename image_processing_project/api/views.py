
# # api/views.py
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# # from image_processing_app.models import Receipt, UploadedImage
# from .serializers import ReceiptSerializer
# from image_processing_app.models import UploadedImage
# from django.apps import apps

# UploadedImage = apps.get_model('image_processing_app', 'UploadedImage')



# class ReceiptListCreateView(APIView):
#     def post(self, request, format=None):
#         merchant_name = request.data.get('merchant_name')
        
#         # Check if merchant name already exists in the database
#         if Receipt.objects.filter(merchant_name=merchant_name).exists():
#             response_data = {
#                 "message": "Merchant name already exists in the database."
#             }
#             return Response(response_data, status=status.HTTP_409_CONFLICT)
        
#         serializer = ReceiptSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             # Custom response message
#             response_data = {
#                 "message": "Details stored in the database successfully."
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)










# class ReceiptListCreateView(APIView):
#     def post(self, request, format=None):
#         merchant_name = request.data.get('merchant_name')
#         serializer = ReceiptSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             receipt_number = ""

#             if merchant_name == 'Walmart':
#                 try:
#                     latest_uploaded_image = UploadedImage.objects.latest('uploaded_at')
#                     extracted_text = latest_uploaded_image.extracted_text
#                     if extracted_text:
#                         # Extract words after "SOLD ITEMS" as receipt number
#                         sold_items_index = extracted_text.find('ITEMS SOLD')
#                         if sold_items_index != -1:
#                             receipt_number = extracted_text[sold_items_index + len('ITEMS SOLD'):].strip()
#                 except UploadedImage.DoesNotExist:
#                     pass

#             # Custom response message
#             response_data = {
#                 "message": "Details stored in the database successfully.",
#                 "receipt_number": receipt_number
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ReceiptSerializer
from image_processing_app.models import UploadedImage

class ReceiptListCreateView(APIView):
    def post(self, request, format=None):
        serializer = ReceiptSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            merchant_name = request.data.get('merchant_name')
            receipt_number = ""

            if merchant_name == 'Walmart':
                try:
                    latest_uploaded_image = UploadedImage.objects.latest('uploaded_at')
                    extracted_text = latest_uploaded_image.extracted_text
                    if extracted_text:
                        tc_index = extracted_text.find('TC#')
                        thc_index = extracted_text.find('TCH')
                        
                        if tc_index != -1:
                            receipt_number = extracted_text[tc_index + len('TC#'):].split()
                        elif thc_index != -1:
                            receipt_number = extracted_text[thc_index + len('TCH'):].split()
                        receipt_number = ' '.join(receipt_number)
                except UploadedImage.DoesNotExist:
                    pass

            # Custom response message
            response_data = {
                "message": "Details stored in the database successfully."
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
