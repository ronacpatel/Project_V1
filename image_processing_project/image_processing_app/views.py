import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .image_reader import ImageReader, Language
from .models import UploadedImage  
from django.http import HttpResponse
from .abc import extract_date, extract_total_and_subtotal 
class ImageExtractionView(APIView):
    def post(self, request, format=None):
        image = request.FILES.get('image')
        
        ir = ImageReader()

        try:
            receipt_info = ir.extract_text(image, lang=Language.ENG)
            
            formatted_receipt_info = receipt_info.replace('\n', '  ')

            
            total_match = re.search(r'\bTOTAL\b', formatted_receipt_info, re.IGNORECASE)
            if total_match:
                total_index = total_match.start()
                total_text = formatted_receipt_info[total_index:]
                total_value = " ".join(total_text.split()[1:])  
                total_value = total_value.replace("\n", "")  
            else:
                total_value = ""
            
            total_value_final = " "
            for i in total_value:
                if i.isalpha():
                    break
                elif i.isdigit() or str(i)=='.':
                    total_value_final = total_value_final + i 

            
            item_descriptions_with_numbers = re.findall(r'([^0-9]+)\s+(\d{12})', formatted_receipt_info)

            
            item_descriptions = []
            seen_descriptions = set()
            for description, _ in item_descriptions_with_numbers:
                description = description.strip()
                if description not in seen_descriptions:
                    seen_descriptions.add(description)
                    item_descriptions.append(description)

            
            date_match = re.search(r'(TCH|TC#)(.*?)$', formatted_receipt_info)
            if date_match:
                date_text = date_match.group(2).strip()
            else:
                date_text = ""

            
            receipt_match = re.search(r'(TCH|TC#)(.+)', formatted_receipt_info)
            if receipt_match:
                receipt_number = receipt_match.group(2).strip()
            else:
                receipt_number = ""

            uploaded_image = UploadedImage(image=image, extracted_text=formatted_receipt_info)
            uploaded_image.save()

            
            first_10_words = formatted_receipt_info.split()[:10]
            walmart_present = any('walmart' in word.lower() for word in first_10_words)

            if walmart_present:
                
                response_data = {
                    'extracted_text': formatted_receipt_info,
                    'receipt_number': receipt_number[:26],
                    'total_value': total_value_final,
                    'item_descriptions': item_descriptions,
                    'date': date_text[29:39]
                }
            else:
                
                date = extract_date(formatted_receipt_info)
                total, subtotal, extracted_text = extract_total_and_subtotal(formatted_receipt_info)
                
                response_data = {
                    'extracted_text': extracted_text,
                    'date': date,
                    'total_value': total,
                    'subtotal_value': subtotal,
                }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




