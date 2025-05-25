from drf_yasg.utils import swagger_auto_schema
from drf_yasg import  openapi




eventchangelogdocs =  swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER, required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Event changelog returned",
                examples={
                    "application/json": {
                        "event_id": 5,
                        "changelog": [
                            {"id": 12, "data": {"title": "Title v1"}, "timestamp": "2025-05-20T10:00:00Z"},
                            {"id": 13, "data": {"title": "Title v2"}, "timestamp": "2025-05-21T10:00:00Z"}
                        ]
                    }
                }
            ),
            403: "Permission denied",
            404: "Event not found"
        },
        operation_description="Returns all previous versions of a given event, sorted by timestamp.",
        tags=["Events - Versioning"]
    )

   
    


eventdiffslog = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('version1_id', openapi.IN_PATH, description="First version ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('version2_id', openapi.IN_PATH, description="Second version ID", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: openapi.Response(
                description="Differences between two versions returned",
                examples={
                    "application/json": {
                        "event_id": 5,
                        "version_id_1": 12,
                        "version_id_2": 13,
                        "diff": {
                            "values_changed": {
                                "root['title']": {
                                    "old_value": "Old Title",
                                    "new_value": "New Title"
                                }
                            }
                        }
                    }
                }
            ),
            400: "Version mismatch or invalid comparison",
            403: "Permission denied",
            404: "Version not found"
        },
        operation_description="Compares two versions of a given event and returns the changes (diff).",
        tags=["Events - Versioning"]
    )

 