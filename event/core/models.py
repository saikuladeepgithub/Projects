
from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='events/',null=True, blank=True)
    is_approved = models.BooleanField(default=False) 
    def __str__(self):
        return self.name

class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.event.name}'
    

class Volunteer(models.Model):
    ACTIVITIES_CHOICES = [
        ('Promotions', 'Promotions'),
        ('Event Management', 'Event Management'),
        ('Crowd Management', 'Crowd Management'),
        # Add more activities as needed
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activities = models.CharField(max_length=200, choices=ACTIVITIES_CHOICES)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.event.name}'
   


# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chats')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat by {self.user.username} on {self.event.name}'

class galleryimages(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='galleries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    caption=models.TextField()

    def __str__(self):
        return f'image by {self.user.username} on {self.event.name}'