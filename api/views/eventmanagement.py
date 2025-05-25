from rest_framework.views import APIView
from api.serializers import EventSerializer, EventVersionSerializer
from rest_framework.response import Response
from rest_framework import status
from api.models import Event, EventCollaborator
from django.db.models import OuterRef, Exists, Subquery, Q, Value
from django.db.models.functions import Coalesce
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from api.docs import createEventdocs, geteventdocs, puteventdocs, createEventbatchdocs



class CreateEventView(APIView):

    permission_classes = [IsAuthenticated]

    @createEventdocs
    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response({"success": "event created successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors},status.HTTP_400_BAD_REQUEST)
    

    @geteventdocs
    def get(self, request, id=None):
        if id is not None:
            try:
                eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=request.user)
            except EventCollaborator.DoesNotExist:
                return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
            serializer = EventSerializer(eventcollaborator.event)
            serializer['role'] = eventcollaborator.role
            return Response({"data":serializer.data}, status.HTTP_200_OK)
        user = request.user
        params = request.query_params

        paginator = PageNumberPagination()
        paginator.page_size = int(params.get('page_size', 10))
        max_page_size = 50
        if paginator.page_size > max_page_size:
            paginator.page_size = max_page_size

        # Filters
        filters = Q()

        # Date range filtering
        start_time = params.get('start_time')
        if start_time:
            filters &= Q(start_time__gte=start_time)

        end_time = params.get('end_time')
        if end_time:
            filters &= Q(end_time__lte=end_time)

        # Title search (case insensitive)
        title = params.get('title')
        if title:
            filters &= Q(title__icontains=title)

        # Filter by recurring or not (expects 'true' or 'false' strings)
        is_recurring = params.get('is_recurring')
        if is_recurring is not None:
            if is_recurring.lower() == 'true':
                filters &= Q(is_recurring=True)
            elif is_recurring.lower() == 'false':
                filters &= Q(is_recurring=False)

        # Sorting - support multiple fields separated by comma
        sort_param = params.get('ordering', 'start_time')  # default sort
        allowed_sort_fields = {'start_time', 'end_time', 'title', 'created_at'}
        sort_fields = []
        for field in sort_param.split(','):
            field = field.strip()
            if not field:
                continue
            direction = ''
            if field.startswith('-'):
                direction = '-'
                field = field[1:]
            if field in allowed_sort_fields:
                sort_fields.append(direction + field)
        if not sort_fields:
            sort_fields = ['start_time']  # fallback

        # Subquery to check if user is collaborator
        collaborator_subquery = EventCollaborator.objects.filter(
            event=OuterRef('pk'),
            collaborators=user
        )

        # Subquery to get the role of user on event
        role_subquery = EventCollaborator.objects.filter(
            event=OuterRef('pk'),
            collaborators=user
        ).values('role')[:1]

        # Annotate event with access and role
        events_qs = Event.objects.annotate(
            has_access=Exists(collaborator_subquery),
            user_role=Coalesce(Subquery(role_subquery), Value('viewer'))
        ).filter(
            has_access=True
        ).filter(
            filters
        ).order_by(*sort_fields)

        page = paginator.paginate_queryset(events_qs, request)

        serialized_events = []
        for event in page:
            data = EventSerializer(event).data
            data['role'] = event.user_role
            serialized_events.append(data)

        return paginator.get_paginated_response(serialized_events)

    @puteventdocs
    def put(self, request, id):
        try:
            eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=request.user, role='editor')
            event = eventcollaborator.event
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_404_NOT_FOUND)
        client_version = request.data.get('version_number')
        if client_version is None:
            return Response({"error": "version_number is required for concurrency control"}, status=status.HTTP_400_BAD_REQUEST)

        if int(client_version) != event.version_number:
            return Response({
                "error": "Version conflict. The event has been modified by another user.",
                "current_version": event.version_number
            }, status=status.HTTP_409_CONFLICT)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            # Check if data changed compared to current event
            updated_data = serializer.validated_data
            current_data = EventSerializer(event).data

            # Remove version_number from comparison
            current_data.pop('version_number', None)
            updated_data.pop('version_number', None)

            # Merge current_data with updated_data for comparison
            merged_data = current_data.copy()
            merged_data.update(updated_data)

            if merged_data == current_data:
                # No actual changes
                return Response({"message": "No changes detected. Update not required."}, status=status.HTTP_200_OK)
        
            with transaction.atomic():
                version_data={
                    'event':event.id,
                    'data':EventSerializer(event).data,
                    'changed_by':request.user.id
                }
                version_serializer = EventVersionSerializer(data=version_data)
                if version_serializer.is_valid():
                    version_serializer.save()
                else:
                    return Response({"error":serializer.errors},status.HTTP_400_BAD_REQUEST)
                event.version_number += 1
                serializer.save(version_number=event.version_number)
                return Response({"success":"event updated successfully", "data":serializer.data}, status.HTTP_202_ACCEPTED)
            
        return Response({"error":serializer.errors},status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, id):
        try:
            eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=request.user, role='owner')
            event = eventcollaborator.event
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response({"message": "event deleted successfully"}, status.HTTP_204_NO_CONTENT)







class EventCreateBatchView(APIView):
    permission_classes=[IsAuthenticated]
    
    @createEventbatchdocs
    def post(self, request):
        events = request.data.get('events', [])
        if not isinstance(events, list) or not events:
            return Response({"error":"invalid data"}, status.HTTP_400_BAD_REQUEST)
        serializer = EventSerializer(data=events, many=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response({"message": "Events created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
