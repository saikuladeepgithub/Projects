from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .forms import FacultyRegistrationForm,ChatMessage,ChatMessageForm
from .models import Faculty,Volunteer
from .forms import FacultyLoginForm
from .models import Event, Review,galleryimages
from .forms import ReviewForm
from .forms import VolunteerForm
from django.shortcuts import render, redirect
from .utils import send_registration_success_email,send_register_volunteer,send_unregister_volunteer
from .forms import EventProposalForm
# Create your views here.

def index(request):
    approved_events = Event.objects.filter(is_approved=True)
    return render(request,'core/base.html',{'events': approved_events})


def login(request):
    if(request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user= auth.authenticate(username=username,password=password)

        if(user is not None):
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Enter valid username,password')
            return redirect('.')
    return render(request,'core/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def student(request):
    if(request.method=='POST'):
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password1=request.POST['password1']
        password2=request.POST['password2']
        username=request.POST['username']
        email=request.POST['email']
        if(username==''):
            messages.info(request,'Username is empty....')
            return redirect('.')
        if(password1==password2):
            if(User.objects.filter(username=username).exists()):
                messages.info(request,'username exists')
                return redirect('.')
            elif(User.objects.filter(email=email).exists()):
                messages.info(request,'email exits')
                return redirect('.')
            else:
                user=User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1)
                
                send_registration_success_email(user.email, user.username)
                user.save()
                return render(request, 'core/registersuccess.html')
        else:
            messages.info(request,'Password not matching....')
            redirect('.')
    return render(request,'core/student.html')

def faculty(request):
    if request.method == 'POST':
        form = FacultyRegistrationForm(request.POST)
        if form.is_valid():
            faculty = form.save(commit=False)
            user = User.objects.create_user(
                username=faculty.username,
                password=form.cleaned_data['password'],
                email=faculty.email,
                first_name=faculty.first_name,
                last_name=faculty.last_name
            )
            faculty.user = user
            faculty.save()
            send_registration_success_email(user.email, user.username)
            return render(request,'core/facultyregistersuccess.html')
    else:
        form = FacultyRegistrationForm()
    return render(request, 'core/faculty.html', {'form': form})

def facultylogin(request):
    if request.method == 'POST':
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')  
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = FacultyLoginForm()
    return render(request, 'core/facultylogin.html', {'form': form})

#def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.reviews.all()
    volunteers = Volunteer.objects.filter(event=event)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be signed in to submit a review or volunteer.')
            return redirect('event_detail', event_id=event.id)
        
        if 'review_submit' in request.POST:
            rform = ReviewForm(request.POST)
            if rform.is_valid():
                review = rform.save(commit=False)
                review.event = event
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted successfully.')
                return redirect('event_detail', event_id=event.id)
        elif 'volunteer_submit' in request.POST:
            existing_volunteer = Volunteer.objects.filter(event=event, user=request.user).exists()
            if existing_volunteer:
                messages.error(request, 'You have already registered as a volunteer for this event.')
                return redirect('event_detail', event_id=event.id)
            vform = VolunteerForm(request.POST)
            if vform.is_valid():
                volunteer = vform.save(commit=False)
                volunteer.event = event
                volunteer.user = request.user
                volunteer.save()
                messages.success(request, 'You have successfully signed up as a volunteer.')
                return redirect('event_detail', event_id=event.id)
    else:
        rform = ReviewForm()
        vform = VolunteerForm()

    return render(request, 'core/event_detail.html', {
        'event': event,
        'reviews': reviews,
        'volunteers': volunteers,
        'rform': rform,
        'vform': vform
    })



#  event chat 
def event_chat(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    chats = event.chats.all().order_by('timestamp')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be signed in to chat.')
            return redirect('event_chat', event_id=event.id)
        
        cform = ChatMessageForm(request.POST)
        if cform.is_valid():
            chat_message = cform.save(commit=False)
            chat_message.event = event
            chat_message.user = request.user
            chat_message.save()
            # messages.success(request, 'Message sent successfully.')
            return redirect('event_chat', event_id=event.id)
    else:
        cform = ChatMessageForm()

    return render(request, 'core/eventchat.html', {
        'event': event,
        'chats': chats,
        'cform': cform,
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, Volunteer

@login_required
def unregister_volunteer(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    volunteer = Volunteer.objects.filter(event=event, user=request.user).first()
    
    if volunteer:
        volunteer.delete()
        send_unregister_volunteer(request.user.email,request.user.username,event)
        messages.success(request, 'You have successfully unregistered as a volunteer.')
    else:
        messages.error(request, 'You are not registered as a volunteer for this event.')
    
    return redirect('event_detail', event_id=event.id)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reviews = event.reviews.all()
    volunteers = Volunteer.objects.filter(event=event)

    # Check if the user is already a volunteer for the event
    is_volunteer = False
    if request.user.is_authenticated:
        is_volunteer = volunteers.filter(user=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be signed in to submit a review or volunteer.')
            return redirect('event_detail', event_id=event.id)
        
        if 'review_submit' in request.POST:
            rform = ReviewForm(request.POST)
            if rform.is_valid():
                review = rform.save(commit=False)
                review.event = event
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted successfully.')
                return redirect('event_detail', event_id=event.id)
        elif 'volunteer_submit' in request.POST:
            vform = VolunteerForm(request.POST)
            if vform.is_valid():
                volunteer = vform.save(commit=False)
                volunteer.event = event
                volunteer.user = request.user
                volunteer.save()
                send_register_volunteer(request.user.email,request.user.username,event.name)
                messages.success(request, 'You have successfully signed up as a volunteer.')
                return redirect('event_detail', event_id=event.id)
    else:
        rform = ReviewForm()
        vform = VolunteerForm()

    return render(request, 'core/event_detail.html', {
        'event': event,
        'reviews': reviews,
        'volunteers': volunteers,
        'rform': rform,
        'vform': vform,
        'is_volunteer': is_volunteer  # Pass the result to the template
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventProposalForm
@login_required
def submit_event_proposal(request):
    if request.method == 'POST':
        form = EventProposalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event proposal submitted successfully!')
            return redirect('submit_event_proposal')  # Replace 'home' with the correct name of your home view
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventProposalForm()

    return render(request, 'core/submit_event_proposal.html', {'form': form})


# Event analysis

from django.shortcuts import render
from .models import Event

def events_analysis(request):
    approved_events = Event.objects.filter(is_approved=True)
    event_data = []

    for event in approved_events:
        reviews_count = event.reviews.count()  # Count the number of reviews
        # Count the number of volunteers
        volunteers_count=Volunteer.objects.filter(event=event).count()
        event_data.append({
            'name': event.name,
            'image': event.image.url if event.image else None,  # Use image URL if exists
            'reviews_count': reviews_count,
            'volunteers_count': volunteers_count,
            'id':event.id
        })

    return render(request, 'core/events_analysis.html', {'event_data': event_data})

def gallery(request):
    events = Event.objects.all()
    return render(request,'core/gallery.html',{
        'events':events,
    })
def gallery_images(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    images=galleryimages.objects.filter(event=event)
    return render(request,'core/gallery_images.html',{
        'images':images,
    })