
# from django.db import models

# class Receipt(models.Model):
#     merchant_name = models.CharField(max_length=200)
#     merchant_address = models.TextField()
#     receipt_number = models.CharField(max_length=50, unique=False)
#     items_purchased = models.TextField()
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.receipt_number

from django.db import models

class Receipt(models.Model):
    merchant_name = models.CharField(max_length=200)
    merchant_address = models.TextField()
    receipt_number = models.CharField(max_length=50, unique=False)
    items_purchased = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)  # Store the extracted text directly in this model

    def __str__(self):
        
        return self.receipt_number
