from rest_framework import viewsets  # Import viewsets from Django REST framework
from rest_framework.response import Response
from .models import CSVFile
from .serializers import CSVFileSerializer
from rest_framework.decorators import action
from django.http import HttpResponse

class CSVFileViewSet(viewsets.ModelViewSet):
    queryset = CSVFile.objects.all()
    serializer_class = CSVFileSerializer

    @action(detail=True, methods=['get', 'post'])
    def download(self, request, pk=None):
        csv_file = self.get_object()
        response = HttpResponse(csv_file.file.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{csv_file.title}"'
        return response

    def create(self, request, *args, **kwargs):
        # Assuming that your CSVFileSerializer handles the file upload.
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
