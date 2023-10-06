
from django.urls import path
from .views import ImageExtractionView

urlpatterns = [
    path('extract/', ImageExtractionView.as_view(), name='extract-image-text'),
]
