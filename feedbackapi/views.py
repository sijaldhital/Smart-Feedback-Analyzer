from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback
from .analyzer import analyze_feedback
from .serializers import FeedbackSerializer


# Create your views here.
def home(request):
    recent_feedbacks = Feedback.objects.all().order_by('-created_at')[:5]
    return render(request, 'feedbackapi/index.html', {'feedbacks': recent_feedbacks})

@api_view(['POST'])
def analyze(request):
    text = request.data.get('text', '').strip()

    if not text:
        return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    sentiment, polarity, keywords, emotion, aspect_sentiments = analyze_feedback(text)

    feedback_data = {
        'text': text,
        'sentiment': sentiment,
        'polarity': polarity,
        'keywords': keywords,
        'emotion': emotion,
        'aspect_sentiments': aspect_sentiments
    }

    serializer = FeedbackSerializer(data=feedback_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def list_feedbacks(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)

