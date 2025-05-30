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
                "range": {"$ref": "#/$defs/range"},
                "date": {"$ref": "#/$defs/date"},
                "time": {"$ref": "#/$defs/time"},
                "dfo": {
                    "type": "object",
                    "properties": {
                        "head": {"$ref": "#/$defs/head"},
                        "body": {"$ref": "#/$defs/body"},
                    },
                    "required": ["head", "body"],

                },
                "fp": {
                    "type": "object",
                    "properties": {
                        "head": {"$ref": "#/$defs/head"},
                        "body": {"$ref": "#/$defs/body"},
                    },
                    "required": ["head", "body"],
                },
                "dfo_Moskva": {
                    "type": "object",
                    "properties": {
                        "head": {"$ref": "#/$defs/head"},
                        "body": {"$ref": "#/$defs/body"},
                    },
                    "required": ["head", "body"],
                },
                "fpk": {
                    "type": "object",
                    "properties": {
                        "head": {"$ref": "#/$defs/head"},
                        "body": {"$ref": "#/$defs/body"},
                    },
                    "required": ["head", "body"],
                },
                "imvd": {
                    "type": "object",
                    "properties": {
                        "head": {"$ref": "#/$defs/head"},
                        "body": {"$ref": "#/$defs/body"},
                    },
                    "required": ["head", "body"],
                },

            },
            "required": ["range", "date", "time", "dfo", "fp", "dfo_Moskva", "fpk", "imvd"],
            "$defs": {
                "range": {"type": "array", "items": {"type": "string"}},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "head": {
                    "type": "object",
                    "properties": {
                        "education_form": {"type": "string"},
                        "education_term": {"type": "string"},
                        "budget": {"type": "string"},
                    },
                    "required": ["education_term", "budget"],
                },
                "specialties": {"type": "array",
                                "items": {"type": "object",
                                          "properties": {
                                              "specialty_name":
                                                  {"type": "string", "specialty_data": {"type": "object"}}
                                          },
                                          "required": ["specialty_name"]
                                          }
                                },
                "faculties": {"type": "array", "items": {"type": "object",
                                                         "properties": {"faculty_name": {"type": "string"},
                                                                        "specialties": {"$ref": "#/$defs/specialties"}
                                                                        },
                                                         "required": ["faculty_name", "specialties"]
                                                         }
                              },
                "educational_institution": {"type": "object",
                                            "properties": {"educational_institution_title": {"type": "string"},
                                                           "faculties": {"$ref": "#/$defs/faculties"}},
                                            "required": ["educational_institution_title", "faculties"]
                                            },
                "body": {"type": "object",
                         "properties": {
                             "educational_institution": {"$ref": "#/$defs/educational_institution"}
                         },
                         "required": ["educational_institution"]}
            },

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
