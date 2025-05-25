from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.serializers import EventSerializer


event_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['title', 'description', 'start_time', 'end_time', 'location', 'is_recurring'],
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, max_length=50, example="Team Sync"),
        'description': openapi.Schema(type=openapi.TYPE_STRING, max_length=500, example="Daily team sync-up"),
        'start_time': openapi.Schema(type=openapi.FORMAT_DATETIME, example="2025-06-01T09:00:00Z"),
        'end_time': openapi.Schema(type=openapi.FORMAT_DATETIME, example="2025-06-01T09:30:00Z"),
        'location': openapi.Schema(type=openapi.TYPE_STRING, max_length=50, example="Zoom"),
        'is_recurring': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'recurrence_pattern': openapi.Schema(type=openapi.TYPE_STRING, max_length=50, example="daily"),
    }
)

event_batch_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['events'],
    properties={
        'events': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=event_schema,
            example=[
                {
                    "title": "Daily Standup",
                    "description": "Morning sync",
                    "start_time": "2025-06-01T09:00:00Z",
                    "end_time": "2025-06-01T09:15:00Z",
                    "location": "Google Meet",
                    "is_recurring": True,
                    "recurrence_pattern": "daily"
                },
                {
                    "title": "Product Review",
                    "description": "Review sprint features",
                    "start_time": "2025-06-02T14:00:00Z",
                    "end_time": "2025-06-02T15:30:00Z",
                    "location": "Room A",
                    "is_recurring": False,
                    "recurrence_pattern": ""
                }
            ]
        )
    }
)



  
createEventdocs = swagger_auto_schema(
        request_body=event_schema,
        responses={
            201: openapi.Response("Event created successfully", event_schema),
            400: "Validation error"
        },
        operation_description="Create a single event.",
        tags=["Events"]
    )
 

geteventdocs = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description='Event ID', type=openapi.TYPE_INTEGER, required=True),
    ],
    responses={200: "OK", 403: "Permission Denied"},
    operation_description="Retrieve a specific event by ID.",
    tags=["Events"]
)



puteventdocs = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Event ID', type=openapi.TYPE_INTEGER, required=True)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['version_number'],
            properties={
                'version_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='Current event version number'),
                # Allow partial updates so other fields can be here dynamically, no strict schema here
            },
            description="Partial event data with required version_number for concurrency control"
        ),
        responses={
            202: openapi.Response("Event updated successfully", EventSerializer),
            400: "Validation error or version_number missing",
            403: "Permission denied",
            404: "Event not found",
            409: "Version conflict"
        },
        operation_description="Update an event with concurrency control using version_number.",
        tags=["Events"]
    )





createEventbatchdocs = swagger_auto_schema(
        request_body=event_batch_request_schema,
        responses={
            201: openapi.Response("Events created successfully", openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Events created successfully"),
                    "data": openapi.Schema(type=openapi.TYPE_ARRAY, items=event_schema)
                }
            )),
            400: "Validation error"
        },
        operation_description="Create multiple events in batch. Accepts a list of event objects under the `events` key.",
        tags=["Events"]
    )
   