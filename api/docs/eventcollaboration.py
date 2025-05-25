from drf_yasg.utils import swagger_auto_schema
from drf_yasg import  openapi




shareEventdocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["collaborators", "role"],
            properties={
                "collaborators": openapi.Schema(type=openapi.TYPE_INTEGER, description="User ID of the collaborator"),
                "role": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Role to assign",
                    enum=["viewer", "editor", "owner"]
                ),
            }
        ),
        responses={
            201: "Event shared successfully",
            403: "Permission denied",
            400: "Validation error"
        },
        operation_description="Share an event with another user and assign them a role.",
        tags=["Events - Sharing"]
    )


geteventpermissiondocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: "Permission retrieved",
            403: "Permission denied",
            404: "Collaborator not found"
        },
        operation_description="Get the role of the current user for a specific event.",
        tags=["Events - Permissions"]
    )


puteventpermissiondocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('user_id', openapi.IN_PATH, description="Collaborator User ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["role"],
            properties={
                "role": openapi.Schema(type=openapi.TYPE_STRING, enum=["viewer", "editor", "owner"])
            }
        ),
        responses={
            202: "Permission updated",
            403: "Permission denied",
            400: "Validation error"
        },
        operation_description="Update the permission role of a collaborator.",
        tags=["Events - Permissions"]
    )



deleteEventpermissiondocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('user_id', openapi.IN_PATH, description="Collaborator User ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            204: "Collaborator removed",
            403: "Permission denied",
            404: "Collaborator not found"
        },
        operation_description="Remove a collaborator from an event.",
        tags=["Events - Permissions"]
    )
   