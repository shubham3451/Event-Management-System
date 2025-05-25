from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("username is required")
        
        email = self.normalize_email(email=email)
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        """
        Checks whether the user has a specific permission.
        """
        return True
    
    def has_module_perms(self, app_label):
        return True
    

class Event(models.Model):
    creator = models.ForeignKey(User, related_name="event_creator", on_delete=models.CASCADE)
    title = models.CharField( max_length=50)
    description = models.CharField(max_length=500)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(null=False, blank=True, max_length=50)
    is_recurring =  models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, null=False, blank=True)
    created_at = models.DateField(auto_now_add=True)
    version_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class EventCollaborator(models.Model):
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('owner', 'Owner'),
    ]
    event = models.ForeignKey(Event, related_name="event_shared", on_delete=models.CASCADE)
    shared_by = models.ForeignKey(User, related_name="event_shared_by", on_delete=models.CASCADE)
    collaborators = models.ForeignKey(User, null=True, blank=True, related_name="collaborators", on_delete=models.DO_NOTHING)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='viewer')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'collaborators')

    def __str__(self):
        return self.shared_by.username


class EventVersion(models.Model):
    event = models.ForeignKey(Event, related_name="versions_event",on_delete=models.CASCADE)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

   