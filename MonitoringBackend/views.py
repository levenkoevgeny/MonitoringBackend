import json

from .serializers import MonitoringDataSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from jsonschema import validate
from rest_framework.decorators import api_view
from rest_framework import permissions


class MonitoringDataFileViewSet(ViewSet):
    serializer_class = MonitoringDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return Response("GET API")

    def create(self, request):

        schema = {
            "type": "object",
            "properties": {
                "range": {"type": "array"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "dfo": {
                    "type": "object",
                    "properties": {
                        "Факультет милиции общественной безопасности": {
                            "type": "object"
                        }
                    },
                    "required": ["Факультет милиции общественной безопасности"],
                },
            },
            "required": ["range", "date", "time", "dfo"],
        }

        file_uploaded = request.FILES.get("file_uploaded")
        with open("monitoring_data/monitoring_data_test.json", "wb+") as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)
        try:
            with open("monitoring_data/monitoring_data_test.json", "r") as file:
                data = json.load(file)
                validate(instance=data, schema=schema)
        except Exception as e:
            print(e)
            return Response(
                "File upload error (wrong format etc.)",
                status=status.HTTP_400_BAD_REQUEST,
            )
        with open("monitoring_data/monitoring_data.json", "wb+") as destination:
            for chunk in file_uploaded.chunks():
                destination.write(chunk)
        return Response("File uploaded successfully!", status=status.HTTP_200_OK)


@api_view(["GET"])
def get_monitoring_data(request):
    with open("monitoring_data/monitoring_data.json", "r") as file:
        data = json.load(file)
    return Response({"data": data}, status=status.HTTP_200_OK)