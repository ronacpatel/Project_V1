
from rest_framework import serializers

class GoogleSheetSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()
    folder_names = serializers.ListField(child=serializers.CharField())
