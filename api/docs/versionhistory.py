from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



eventhistorydocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Event ID', type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('version_id', openapi.IN_PATH, description='Version ID', type=openapi.TYPE_INTEGER, required=True),
        ],
        operation_description="Get a specific version of an event by event ID and version ID.",
        responses={
            200: openapi.Response(description="Version data retrieved successfully"),
            403: "Permission denied",
            404: "Version not found"
        },
    )


eventrollbackdocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Event ID', type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('version_id', openapi.IN_PATH, description='Version ID to rollback to', type=openapi.TYPE_INTEGER, required=True),
        ],
        operation_description="Rollback an event to a specific version.",
        responses={
            201: openapi.Response(description="Event rolled back successfully"),
            400: "Bad request or validation error",
            403: "Permission denied",
            404: "Version not found"
        },
        tags=["Event Versioning"]
    )


