# Models for handling general site contact form messages
from django.db import models

class ContactMessage(models.Model):
    """
    Stores feedback and inquiries sent by visitors via the Contact Us form.
    """
    subject = models.CharField(max_length=200)
    body = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject}--{self.body[:20]}"