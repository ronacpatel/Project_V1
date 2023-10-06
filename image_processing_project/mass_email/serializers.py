

from rest_framework import serializers
from .models import Email
import re

class EmailSerializer(serializers.ModelSerializer):
    cc = serializers.CharField(required=False, allow_blank=True)
    bcc = serializers.CharField(required=False, allow_blank=True)

    def validate_cc(self, value):
        email_regex = r'^\S+@\S+\.\S+$'
        ccs = [email.strip() for email in value.split(',') if email]
        for cc in ccs:
            if not re.match(email_regex, cc):
                raise serializers.ValidationError('Invalid email address in CC')
        return value

    def validate_bcc(self, value):
        email_regex = r'^\S+@\S+\.\S+$'
        bccs = [email.strip() for email in value.split(',') if email]
        for bcc in bccs:
            if not re.match(email_regex, bcc):
                raise serializers.ValidationError('Invalid email address in BCC')
        return value

    class Meta:
        model = Email
        fields = ('username', 'password', 'subject', 'message', 'recipients', 'cc', 'bcc')
