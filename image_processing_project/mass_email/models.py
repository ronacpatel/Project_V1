from django.db import models



# Create your models here.
from django.db import models

class Email(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    recipients = models.TextField()  # Store recipients as a comma-separated string
    cc = models.TextField()
    bcc = models.TextField()
    

    def get_recipient_list(self):
        return [email.strip() for email in self.recipients.split(',')]
