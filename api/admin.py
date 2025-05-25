from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, EventCollaborator, EventVersion

# Minimal custom UserAdmin
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()  # ✅ Avoid errors related to groups/user_permissions

admin.site.register(User, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creator', 'start_time', 'end_time', 'is_recurring', 'created_at', 'version_number')
    search_fields = ('title', 'creator__username')
    list_filter = ('is_recurring', 'created_at')
    ordering = ('-created_at',)


@admin.register(EventCollaborator)
class EventCollaboratorAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'shared_by', 'collaborators', 'role', 'created_at')
    search_fields = ('event__title', 'shared_by__username', 'collaborators__username')
    list_filter = ('role', 'created_at')


@admin.register(EventVersion)
class EventVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'timestamp', 'changed_by')
    list_filter = ('timestamp',)
    search_fields = ('event__title', 'changed_by__username')
