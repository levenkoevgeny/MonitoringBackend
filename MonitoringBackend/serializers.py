from rest_framework.serializers import Serializer, FileField


class MonitoringDataSerializer(Serializer):
    file_uploaded = FileField()

    class Meta:
        fields = ["file_uploaded"]