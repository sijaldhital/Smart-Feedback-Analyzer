from django.db import models

# Create your models here.
class Feedback(models.Model):
    text = models.TextField()
    sentiment = models.CharField(max_length=20)
    polarity = models.FloatField()
    keywords = models.TextField(blank=True)
    emotion = models.CharField(max_length=20, blank=True)
    aspect_sentiments = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} - {self.sentiment}"
    