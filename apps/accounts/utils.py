from mailjet_rest import Client
from django.conf import settings

def send_email(subject, text_content, recipient_email):
    mailjet = Client(auth=(settings.MAILJET_API_KEY, settings.MAILJET_API_SECRET), version='v3.1')
    data = {
      'Messages': [
        {
          "From": {
            "Email": "therbsol@therbsolutions.com",  
            "Name": "Your Name or Company Name"
          },
          "To": [
            {
              "Email": recipient_email,
              "Name": "Recipient Name"
            }
          ],
          "Subject": subject,
          "TextPart": text_content,
        }
      ]
    }
    result = mailjet.send.create(data=data)
    return result.status_code, result.json()
