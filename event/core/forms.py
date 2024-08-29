# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Faculty
from .models import Review
from .models import Volunteer
class FacultyRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Faculty
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def save(self, commit=True):
        faculty = super(FacultyRegistrationForm, self).save(commit=False)
        if commit:
            faculty.save()
        return faculty


class FacultyLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['activities', 'phone_number']
        widgets = {
            'activities': forms.Select(),
        }



# forms.py
from django import forms
from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'Enter your message here'}),
        }


from django import forms
from .models import Event

class EventProposalForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'image']
