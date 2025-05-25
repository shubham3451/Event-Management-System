from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import EventSerializer, EventVersionSerializer
from api.models import EventVersion, EventCollaborator
from django.shortcuts import get_object_or_404
from api.docs import eventhistorydocs, eventrollbackdocs

class EventsHistoryView(APIView):
    
    """
    Retrieve the data of a specific historical version of an event.

    - Requires the user to be a collaborator on the event.
    - Returns the historical version data in full detail.
    """
    permission_classes = [IsAuthenticated]

    @eventhistorydocs
    def get(self, request, id, version_id):
        try:
            event_id=id
            EventCollaborator.objects.select_related('event').get(event__id=event_id, collaborators=request.user, role__in=['viewer', 'editor', 'owner'])
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        eventversion = get_object_or_404(EventVersion, event__id=event_id,id=version_id)
        if eventversion:
            return Response({"data": eventversion.data}, status.HTTP_200_OK)
        return Response({"message":"no matching version found"}, status.HTTP_204_NO_CONTENT)
    
class EventsRollbackView(APIView):
  
    """
    Rollback an event to a specific historical version.

    - Only allowed for users with 'editor' or 'owner' roles.
    - Saves the current state as a new version after rollback.
    """
    permission_classes = [IsAuthenticated]

    @eventrollbackdocs
    def post(self, request, id, version_id):
        try:
           event_id=id
           eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=event_id, collaborators=request.user, role__in=['editor', 'owner'])
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        eventversion = get_object_or_404(EventVersion, event__id=event_id,id=version_id)
        event = eventcollaborator.event
        serializer = EventSerializer(event, data=eventversion.data, partial=False )
        if serializer.is_valid():
            serializer.save()
            current_data = EventSerializer(event).data
            version_data = {
            'event': event.id,
            'data': current_data,
            'changed_by': request.user.id
        }
            eventversionserializer = EventVersionSerializer(data=version_data)
            if eventversionserializer.is_valid():
                eventversionserializer.save()
                return Response({"message": "Events rollbacked successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

    


