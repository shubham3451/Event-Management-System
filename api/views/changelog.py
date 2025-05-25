from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.serializers import *
from api.models import EventVersion
from django.shortcuts import get_object_or_404
from deepdiff import DeepDiff
from api.docs import eventchangelogdocs, eventdiffslog


class EventsChangeLogView(APIView):
  
    """
    Get the version history (changelog) of a specific event.
    """
    permission_classes = [IsAuthenticated]
    
    @eventchangelogdocs
    def get(self, request, id):
        try:
            event_id=id
            EventCollaborator.objects.select_related('event').get(event__id=event_id, collaborators=request.user, role__in=['viewer', 'editor', 'owner'])
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        
        versions = EventVersion.objects.filter(event__id=event_id).order_by('-timestamp')
        serializer = EventVersionSerializer(versions, many=True)

        return Response({
            "event_id": event_id,
            "changelog": serializer.data
        }, status=status.HTTP_200_OK)
    

    
class EventsDiffView(APIView):

    """
    Compare two versions of the same event and return the difference.
    """
    permission_classes = [IsAuthenticated]
    
    @eventdiffslog
    def get(self, request, id, version1_id, version2_id):
        
        try:
            event_id=id
            EventCollaborator.objects.select_related('event').get(event__id=event_id, collaborators=request.user, role__in=['viewer', 'editor', 'owner'])
        except EventCollaborator.DoesNotExist:
            return Response({"error":"permission denied"}, status.HTTP_403_FORBIDDEN)
        
        version1 = get_object_or_404(EventVersion, id=version1_id)
        version2 = get_object_or_404(EventVersion, id=version2_id)
        if version1.event.id != version2.event.id or version1.event.id != int(id):
            return Response(
                {"error": "Version IDs do not belong to the same event."},
                status=status.HTTP_400_BAD_REQUEST
            )

        diff = DeepDiff(version1.data, version2.data, ignore_order=True).to_dict()

        return Response({
            "event_id": id,
            "version_id_1": version1_id,
            "version_id_2": version2_id,
            "diff": diff
        }, status=status.HTTP_200_OK)

