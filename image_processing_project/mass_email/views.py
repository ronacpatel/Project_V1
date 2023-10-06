

import smtplib
import re
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
from email import encoders
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Email
from .serializers import EmailSerializer

@api_view(['POST'])
def send_email(request):
    serializer = EmailSerializer(data=request.data)

    if serializer.is_valid():
        email_data = serializer.validated_data

        recipients_str = email_data.get('recipients', '')
        cc_str = email_data.get('cc', '') or ''  
        bcc_str = email_data.get('bcc', '') or ''  

        recipients = [email.strip() for email in recipients_str.split(',') if email]
        cc = [email.strip() for email in cc_str.split(',') if email]
        bcc = [email.strip() for email in bcc_str.split(',') if email]

        valid_recipients = []
        invalid_recipients = []

        # email_regex = r'^\S+@\S+\.\S+$'
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


        for recipient in recipients:
            if re.match(email_regex, recipient):
                valid_recipients.append(recipient)
            else:
                invalid_recipients.append(recipient)

        valid_cc = [email for email in cc if re.match(email_regex, email)]
        valid_bcc = [email for email in bcc if re.match(email_regex, email)]

        try:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587  # Use 465 for SSL or 587 for TLS
            smtp_username = email_data['username']
            # smtp_password = 'qklt fmie jhvg seic'  
            smtp_password = email_data['password']
            from_email = email_data['username']
            subject = email_data['subject']
            message = email_data['message']

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = ', '.join(valid_recipients)
            msg['Cc'] = ', '.join(valid_cc) if valid_cc else ''
            msg['Bcc'] = ', '.join(valid_bcc) if valid_bcc else ''
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            attachments = request.FILES.getlist('attachments', [])
            if attachments:
                for attachment in attachments:
                    filename = attachment.name
                    content = attachment.read()

                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(content)
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(part)

            recipients = valid_recipients

            recipients += valid_cc
            recipients += valid_bcc

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, recipients, msg.as_string())
            server.quit()

            if invalid_recipients:
                return Response({'message': 'Emails sent with some invalid recipients', 'invalid_recipients': invalid_recipients}, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                return Response({'message': 'Emails sent successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
