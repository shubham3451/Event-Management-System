from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import EventCollaborationSerializer
from api.models import EventCollaborator, Event
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from api.docs import shareEventdocs, geteventpermissiondocs, puteventpermissiondocs, deleteEventpermissiondocs




class ShareEventView(APIView):

    """
    Share an event with another user and assign a role.
    """
    permission_classes = [IsAuthenticated]

    @shareEventdocs
    def post(self, request, id):
        
        event =  get_object_or_404(Event, id=id)
        if event.creator != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventCollaborationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(shared_by=request.user, event=event)
            return Response({"success":"event shared successfully", "data":serializer.data}, status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status.HTTP_400_BAD_REQUEST)
    





class EventPermissionView(APIView):

    """
    View, update, or remove a user's permission for an event.
    """
    permission_classes = [IsAuthenticated]

    @geteventpermissiondocs
    def get(self, request, id):
        try:
            eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=request.user,role__in=['viewer','editor', 'owner'])
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
    
        permission = eventcollaborator.role
        collaborator = eventcollaborator.collaborators.username
        return Response({"data":{"user":collaborator, "role":permission}}, status.HTTP_200_OK)
    


    @puteventpermissiondocs
    def put(self, request, id, user_id):
        try:
            EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=request.user, role__in=['editor', 'owner'])
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        try:
            eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=id, collaborators__id=user_id)
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        
        serializer = EventCollaborationSerializer(eventcollaborator, data=request.data, partial=True)
        if serializer.is_valid():
            return Response({"message":"permission updated successfully", "data":serializer.data}, status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @deleteEventpermissiondocs
    def delete(self, request, id, user_id):
        try:
            EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=request.user, role='owner')
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        try:
            eventcollaborator = EventCollaborator.objects.select_related('event').get(event__id=id, collaborators=user_id)
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        eventcollaborator.delete()
        return Response({"message": "event deleted successfully"}, status.HTTP_204_NO_CONTENT)