# applications/forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, F
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class JobApplicationForm(forms.ModelForm):
    ph_num = PhoneNumberField()
    available_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = JobApplication
        fields = '__all__'
        exclude = ['user', 'job', 'slug']

    def __init__(self, *args, **kwargs):
        super(JobApplicationForm, self).__init__(*args, **kwargs)
        
        # Make email and username readonly
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True

class JobForm(forms.ModelForm):
    job_release_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    job_closing_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Job
        exclude = ['released_by']  

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

    
class ScheduleMeetingForm(forms.ModelForm):
    job_application = forms.CharField(widget=forms.HiddenInput(), required=False)
    scheduled_meet_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    scheduled_meet_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    scheduled_meet_attendees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
             Q(profile__is_teamlead=True) | Q(profile__is_teamMember=True) 
        ),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = MeetingSchedule
        fields = ['scheduled_meet_date', 'scheduled_meet_time', 'scheduled_meet_link', 'scheduled_meet_attendees']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ScheduleMeetingForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['job_application'].initial = f"{user.first_name} {user.last_name}"
            self.fields['job_application'].widget.attrs['readonly'] = True


class MeetingReviewForm(forms.ModelForm):
    class Meta:
        model = MeetingReview
        fields = ['decision', 'reason']
        widgets = {
            'decision': forms.RadioSelect(choices=[('accept', 'Accept'), ('reject', 'Reject')]),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

class TeamLeadDecisionForm(forms.ModelForm):
    class Meta:
        model = TeamLeadDecision
        fields = ['decision', 'reason']
        widgets = {
            'decision': forms.RadioSelect(choices=TeamLeadDecision.DECISION_CHOICES),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

class ManagerDecisionForm(forms.Form):
    DECISION_CHOICES = [
        ('accept_with_meeting', 'Accept with Meeting'),
        ('accept_without_meeting', 'Accept without Meeting'),
        ('reject', 'Reject'),
    ]

    decision = forms.ChoiceField(choices=DECISION_CHOICES, widget=forms.RadioSelect)
    approved_by_manager = forms.BooleanField(label='Approved by Manager', required=False)
    reason = forms.CharField(widget=forms.Textarea, required=False)
    meeting_link = forms.URLField(required=False)
    meeting_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    meeting_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the 'required' attribute dynamically based on the selected decision
        if 'decision' in self.data:
            decision = self.data['decision']
            if decision == 'accept_with_meeting':
                self.fields['meeting_link'].required = True
                self.fields['meeting_time'].required = True


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    applicant = forms.CharField(widget=forms.HiddenInput())  # Hidden input for the applicant name
    to_email = forms.EmailField(widget=forms.HiddenInput()) 