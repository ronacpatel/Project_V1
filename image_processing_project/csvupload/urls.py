from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CSVFileViewSet

router = DefaultRouter()
router.register(r'csv', CSVFileViewSet)

urlpatterns = [
    path('csv/', include(router.urls)),
]
