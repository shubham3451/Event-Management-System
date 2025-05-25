from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    # -------------------- Authentication --------------------
    path('api/auth/register',SignUpView.as_view(), name='auth-register'),# POST
    path('api/auth/login', LoginView.as_view(), name='auth-login'), # POST
    path('api/auth/refresh',TokenRefreshView.as_view(), name='auth-refresh'),
    path('api/auth/logout', LogoutView.as_view(), name='auth-logout'), # POST

    # -------------------- Event Management --------------------
    path('api/events', CreateEventView.as_view(), name='event-list-create'),  # POST
    path('api/events/<int:id>', CreateEventView.as_view(), name='event-detail'),  # GET, PUT, DELETE
    path('api/events/', CreateEventView.as_view(), name='event-detail'),  # GET All
    path('api/events/batch', EventCreateBatchView.as_view(), name='event-batch-create'),  # POST

    # -------------------- Collaboration --------------------
    path('api/events/<int:id>/share', ShareEventView.as_view(), name='event-share'),  # POST
    path('api/events/<int:id>/permissions', EventPermissionView.as_view(), name='event-permissions-list'),  # GET
    path('api/events/<int:id>/permissions/<int:user_id>', EventPermissionView.as_view(), name='event-permission-update'),  # PUT
    path('api/events/<int:id>/permissions/<int:user_id>', EventPermissionView.as_view(), name='event-permission-remove'),  # DELETE

    # -------------------- Version History --------------------
    path('api/events/<int:id>/history/<int:version_id>', EventsHistoryView.as_view(), name='event-version-detail'),  # GET
    path('api/events/<int:id>/rollback/<int:version_id>',EventsRollbackView.as_view(), name='event-version-rollback'),  # POST

    # -------------------- Changelog & Diff --------------------
    path('api/events/<int:id>/changelog', EventsChangeLogView.as_view(), name='event-changelog'),  # GET
    path('api/events/<int:id>/diff/<int:version1_id>/<int:version2_id>', EventsDiffView.as_view(), name='event-diff'),  # GET

    
]
