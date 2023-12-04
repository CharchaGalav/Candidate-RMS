from django.views.generic import View
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from .forms import *
from .models import *

from django.urls import reverse_lazy

class home(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

class AllJobs(generic.ListView):
    model = Job
    template_name = 'all_jobs.html'
    context_object_name = 'jobs'
    
class JobDetail(generic.DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_has_applied = False
        if self.request.user.is_authenticated:
            user_has_applied = JobApplication.objects.filter(user=self.request.user, job=context['job']).exists()
        context['user_has_applied'] = user_has_applied
        return context

    
class ApplyNowView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, job_id):
        job = Job.objects.get(pk=job_id)
        user = request.user
        initial_data = {'user': user, 'username': user.username, 'email': user.email}
        form = JobApplicationForm(initial=initial_data)
        return render(request, 'apply.html', {'form': form, 'job': job})

    def post(self, request, job_id):
        
        job = Job.objects.get(pk=job_id)
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            job_application = form.save(commit=False)
            job_application.user = request.user
            job_application.job = job
            job_application.logs = timezone.localtime(timezone.now())
            job_application.save()
            # print(job_application)
            return redirect('all_jobs')
            
        return render(request, 'apply.html', {'form': form, 'job': job})

class AppliedJobs(LoginRequiredMixin, View):
    template_name = 'applied_jobs.html'

    def get(self, request):
        user = request.user
        job_applications = JobApplication.objects.filter(user=user)
        return render(request, self.template_name, {'job_applications': job_applications})

class CustomLoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                job_id = request.GET.get('job_id')
                if job_id:
                    return redirect('apply', job_id=job_id)
                else:
                    return redirect('home')
        return render(request, self.template_name, {'form': form})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('all_jobs')

class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('custom_login')  # Redirect to login page after registration
        return render(request, self.template_name, {'form': form})


class ReleaseJobView(View):
    template_name = 'release_job.html'

    def get(self, request):
        if not request.user.is_authenticated or not request.user.profile.is_hr:
            return redirect('home')  

        form = JobForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if not request.user.is_authenticated or not request.user.profile.is_hr:
            return redirect('home')

        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.released_by = request.user
            job.save()
            request.user.profile.released_jobs = job
            request.user.profile.save()
            return redirect('all_jobs')  

        return render(request, self.template_name, {'form': form})


class ViewJobApplications(UserPassesTestMixin, View):
    template_name = 'view_job_applications.html'

    def test_func(self):
        return self.request.user.is_authenticated 

    def get(self, request):
        user = request.user
        job_info_with_applicants = []

        if user.profile.is_hr:
            released_jobs = Job.objects.filter(released_by=user)
        elif user.profile.is_teamlead or user.profile.is_teamMember or user.profile.is_manager or user.profile.is_mainHr or user.profile.is_onboardingHr:
            released_jobs = Job.objects.filter(released_by__profile__is_hr=True) 

        for job in released_jobs:
            job_info = {
                'job_name': job.job_name,
                'job_location': job.job_location,
                'job_type': job.get_job_type_display(),
                'slug': job.slug,  
            }
            applicants = JobApplication.objects.filter(job=job)

            job_info['applicants'] = applicants
            job_info_with_applicants.append(job_info)

        return render(request, self.template_name, {'jobs_with_applicants': job_info_with_applicants})


class ViewApplicants(View):
    template_name = 'view_applicants.html'

    def get(self, request, job_slug):
        job = get_object_or_404(Job, slug=job_slug)
        if self.request.user.profile.is_hr:
            applicants = JobApplication.objects.filter(job=job)
        elif self.request.user.profile.is_teamlead or self.request.user.profile.is_teamMember:
            applicants = JobApplication.objects.filter(job=job, hr_is_accepted = True)
        elif self.request.user.profile.is_manager:
            applicants = JobApplication.objects.filter(job=job, teamlead_is_accepted = True)
        elif self.request.user.profile.is_mainHr:
            applicants = JobApplication.objects.filter(job=job, manager_is_accepted = True)
        form = ScheduleMeetingForm()
        return render(request, self.template_name, {'job': job, 'applicants': applicants , 'form': form})
    
    def post(self, request, job_slug):
        job = get_object_or_404(Job, slug=job_slug)
        applicants = JobApplication.objects.filter(job=job)
        form = ScheduleMeetingForm(request.POST)

        if form.is_valid():
            meeting_schedule = form.save(commit=False)
            
            job_application_slug = form.cleaned_data['job_application']
            job_application = get_object_or_404(JobApplication, slug=job_application_slug)
            
            meeting_schedule.job_application = job_application
            meeting_schedule.scheduled_by = request.user
            meeting_schedule.save()
            meeting_schedule.scheduled_meet_attendees.set(form.cleaned_data['scheduled_meet_attendees'])
            
            meeting_schedule.logs = timezone.now()

            meeting_schedule.save()
            
            send_mail(
                f"Meeting scheduled for {meeting_schedule.job_application.f_name} {meeting_schedule.job_application.l_name}",
                f"A meeting has been scheduled for {meeting_schedule.job_application.f_name} "
                f"{meeting_schedule.job_application.l_name} on {meeting_schedule.scheduled_meet_date}. "
                f"Please join using this link: {meeting_schedule.scheduled_meet_link}",
                'EMAIL_HOST_USER',
                [meeting_schedule.job_application.email],
                fail_silently=False,
            )
            print(meeting_schedule.job_application.f_name)
            self.send_email_to_attendees(meeting_schedule.scheduled_meet_attendees.all(), meeting_schedule)
            return render(request, self.template_name, {'job': job, 'applicants': applicants, 'form': form})
    
            applicants = JobApplication.objects.filter(job=job)
        return render(request, self.template_name, {'job': job, 'applicants': applicants, 'form': form})
      

    def send_email_to_attendees(self, attendees, meeting_schedule):
        from_email = 'EMAIL_HOST_USER'
        for attendee in attendees:
            to_email = attendee.email
            print(to_email)
            subject = f"Meeting scheduled for {meeting_schedule.job_application.f_name} {meeting_schedule.job_application.l_name}"
            message = f"Hi {attendee.first_name},\n\n" \
                      f"A meeting has been scheduled for {meeting_schedule.job_application.f_name} " \
                      f"{meeting_schedule.job_application.l_name} on {meeting_schedule.scheduled_meet_date}. " \
                      f"Please join using this link: {meeting_schedule.scheduled_meet_link}"
            count = send_mail(subject, message, from_email, [to_email])
            if count > 0:
                print("Email sent successfully!")
            else:       
                print("Email not sent.")


class ViewProfile(LoginRequiredMixin, View):
    template_name = 'view_profile.html'

    def get(self, request, applicant_slug):
        form = ManagerDecisionForm()
        job_application = get_object_or_404(JobApplication, slug=applicant_slug)
        
        return render(request, self.template_name, {'application': job_application})

    def post(self, request, applicant_slug):
        job_application = get_object_or_404(JobApplication, slug=applicant_slug)
        form = ManagerDecisionForm(request.POST)

        # Accept action
        if 'accept' in request.POST:
            if not job_application.hr_is_accepted:
                job_application.hr_is_accepted = True
                job_application.save()  

        # Reject action
        elif 'reject' in request.POST:
            form = RejectionDetailsForm(request.POST)
            if form.is_valid():
                # print("Form is valid")
                rejection_details = form.save(commit=False)
                rejection_details.job_application = job_application
                rejection_details.rejected_by = request.user
                rejection_details.logs = timezone.localtime(timezone.now())
                rejection_details.save()
                if job_application.hr_is_accepted == True:
                    job_application.hr_is_accepted = False
                    job_application.save()
                return redirect('view_applicants' , job_slug=job_application.job.slug)
            
        
        elif 'givedecision' in request.POST:
            form = ManagerDecisionForm(request.POST)
            if form.is_valid():
                    print("Form is valid")
                    decision = form.cleaned_data['decision']
                    print("DEcsion")
                    meeting_link = form.cleaned_data.get('meeting_link', '')
                    meeting_date = form.cleaned_data.get('meeting_date', '')
                    meeting_time = form.cleaned_data.get('meeting_time', '')

                    applicant_user = User.objects.get(username=job_application.user)
                    
                    decision_instance = ManagerDecision(
                        applicant=job_application.user,
                        decision=form.cleaned_data['decision'],
                        reason=form.cleaned_data.get('reason', ''),
                        meeting_link=meeting_link,
                        meeting_date=meeting_date,
                        meeting_time=meeting_time,
                        email=applicant_user.email,
                    )
                    decision_instance.save()
                    job_application.manager_is_accepted = True
                    job_application.save()
                    if decision == 'accept_with_meeting':
                        # Send email to applicant
                        send_mail(
                            f"Meeting scheduled for {job_application.user}",
                            f"A meeting has been scheduled for {job_application.user} on {meeting_date} at {meeting_time}. "
                            f"Please join using this link: {meeting_link}",
                            'EMAIL_HOST_USER',
                            [applicant_user.email],
                            fail_silently=False,
                        )
                    return redirect('home')
         

        return render(request, self.template_name, {'application': job_application, 'form': form})


class AllAcceptedCandidates(UserPassesTestMixin, View):
    template_name = 'all_accepted_candidates.html'

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.profile.is_hr or self.request.user.profile.is_teamlead or self.request.user.profile.is_manager)

    def get(self, request):
        user = self.request.user
        if user.profile.is_hr:
            accepted_candidates = JobApplication.objects.filter(hr_is_accepted=True)
            print(accepted_candidates)
        elif user.profile.is_teamlead:
            accepted_candidates = JobApplication.objects.filter(teamlead_is_accepted=True)
        elif user.profile.is_manager:
            accepted_candidates = JobApplication.objects.filter(manager_is_accepted=True)
        else:
            accepted_candidates = JobApplication.objects.none()

        return render(request, self.template_name, {'candidates': accepted_candidates})


class AllRejectedCandidates(UserPassesTestMixin, View):
    template_name = 'all_rejected_candidates.html'

    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.profile.is_hr or
            self.request.user.profile.is_teamlead or
            self.request.user.profile.is_manager
        )

    def get(self, request):
        user = self.request.user
        if user.profile.is_hr:
            rejected_candidates = RejectionDetails.objects.filter(rejected_by=user)
            print(rejected_candidates)
        elif user.profile.is_teamlead:
            rejected_candidates = RejectionDetails.objects.filter(rejected_by=user)
        elif user.profile.is_manager:
            rejected_candidates = RejectionDetails.objects.filter(rejected_by=user)
        else:
            rejected_candidates = RejectionDetails.objects.none()

        return render(request, self.template_name, {'candidates': rejected_candidates, 'status': 'Rejected'})


class ViewScheduledMeetings(UserPassesTestMixin, View):
    template_name = 'view_scheduled_meetings.html'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.profile.is_hr or user.profile.is_teamlead or user.profile.is_teamMember)

    def get(self, request):
        user = self.request.user
        if user.profile.is_hr:
            meetings = MeetingSchedule.objects.filter(scheduled_by=user)
        elif user.profile.is_teamlead:
            meetings = MeetingSchedule.objects.filter(scheduled_meet_attendees=user)
        elif user.profile.is_teamMember:
            meetings = MeetingSchedule.objects.filter(scheduled_meet_attendees=user)
        else:
            meetings = MeetingSchedule.objects.none()

        return render(request, self.template_name, {'meetings': meetings})
    
class ReviewMeetingView(LoginRequiredMixin, View):
    template_name = 'review_meeting.html'

    def get(self, request, applicant_slug):
        meeting = MeetingSchedule.objects.get(job_application__slug=applicant_slug)
        form = MeetingReviewForm(initial={'reviewer': request.user})  # Set the initial value for reviewer
        return render(request, self.template_name, {'form': form, 'meeting': meeting})

    def post(self, request, applicant_slug):
        meeting = MeetingSchedule.objects.get(job_application__slug=applicant_slug)
        form = MeetingReviewForm(request.POST)

        if form.is_valid():
            decision = form.cleaned_data['decision']
            reason = form.cleaned_data['reason']

            meeting_review = form.save(commit=False)
            meeting_review.meeting_schedule = meeting
            meeting_review.reviewer = request.user  # Set the reviewer to the logged-in user
            meeting_review.save()

            return redirect('view_scheduled_meetings')

        return render(request, self.template_name, {'form': form, 'meeting': meeting})
    
class AllCandidateReviewsView(View):
    template_name = 'all_candidate_reviews.html'

    def get(self, request):
        user = self.request.user

        if user.profile.is_teamlead:
            # Assuming the team lead is scheduled as an attendee
            meetings = MeetingSchedule.objects.filter(scheduled_meet_attendees=user)
            reviews = MeetingReview.objects.all()

            # Get distinct list of applicants
            distinct_applicants = MeetingReview.objects.all().values(
                'meeting_schedule__job_application__id',
                'meeting_schedule__job_application__f_name',
                'meeting_schedule__job_application__l_name',
                'meeting_schedule__job_application__job__job_name'
                
            ).annotate(num_reviews=Count('id'))

            return render(request, self.template_name, {'distinct_applicants': distinct_applicants})

        return render(request, self.template_name, {'distinct_applicants': []})

class CandidateReviewsView(View):
    template_name = 'candidate_reviews.html'

    def get(self, request, applicant_id):
        user = self.request.user
        applicant_reviews = MeetingReview.objects.filter(meeting_schedule__job_application=applicant_id)
        applicant = JobApplication.objects.get(id=applicant_id)
        return render(request, self.template_name, {'reviews': applicant_reviews, 'applicant_id': applicant_id, 'applicant': applicant})
    
    def post(self, request, applicant_id):
        job_application = get_object_or_404(JobApplication, id=applicant_id)

        # Accept action
        if 'accept' in request.POST:
            if not job_application.teamlead_is_accepted:
                job_application.teamlead_is_accepted = True
                job_application.save()  

        # Reject action
        elif 'reject' in request.POST:
            form = RejectionDetailsForm(request.POST)
            if form.is_valid():
                print("Form is valid")
                rejection_details = form.save(commit=False)
                rejection_details.job_application = job_application
                rejection_details.rejected_by = request.user
                rejection_details.logs = timezone.localtime(timezone.now())
                rejection_details.save()
                if job_application.teamlead_is_accepted == True:
                    job_application.teamlead_is_accepted = False
                    job_application.save()
                return redirect('all_candidate_reviews')
        
        return render(request, self.template_name, { 'applicant_id': applicant_id})  


class AcceptedCandidatesbyManager(View):
    template_name = 'accepted_candidate_by_manager.html'

    def get(self, request):
        user = self.request.user
        if user.profile.is_mainHr or user.profile.is_manager  or user.profile.is_onboardingHr:
            accepted_candidates = ManagerDecision.objects.filter(decision='accept_with_meeting' or 'accept_without_meeting')
            # Retrieve relevant information for each candidate
            candidate_data = []
            for decision in accepted_candidates:
                candidate_data.append({
                    'applicant_id': decision.id,
                    'applicant': decision.applicant,
                    'decision': decision.decision,
                    'reason': decision.reason,
                    'meeting_link': decision.meeting_link,
                    'meeting_date': decision.meeting_date,
                    'meeting_time': decision.meeting_time,
                })

            return render(request, self.template_name, {'candidates_data': candidate_data})
        else:
            return redirect('home')
        
# class SendEmail(generic.FormView):
#     template_name = 'send_email.html'

#     form_class = EmailForm
#     success_url = reverse_lazy('home')  # Redirect to home after sending email
    
#     def get(self, request, pk):
#         applicant = get_object_or_404(ManagerDecision, pk=pk)
#         form = EmailForm(initial={'applicant': applicant, pk: pk})
#         return render(request, self.template_name, {'form': form, 'applicant': applicant})
    
#     def form_valid(self, form, pk):
#         subject = form.cleaned_data['subject']
#         message = form.cleaned_data['message']
#         sender_name = self.request.user.username


#         # Save the data to the EmailLog model
#         EmailLog.objects.create(
#             applicant=,
#             sender_name=sender_name,
#             to_email=,
#             subject=subject,
#             message=message
#         )
#         return super().form_valid(form)
    

class SendEmail(generic.FormView):
    template_name = 'send_email.html'
    form_class = EmailForm
    success_url = reverse_lazy('home')  # Redirect to home after sending email
    
    def get(self, request, pk):
        # Retrieve the ManagerDecision object
        applicant = get_object_or_404(ManagerDecision, pk=pk)
        # Initialize the form with the applicant information
        form = EmailForm(initial={'applicant': applicant.applicant, 'to_email': applicant.email})
        return render(request, self.template_name, {'form': form, 'applicant': applicant})
    
    def form_valid(self, form):
        # Extract data from the form
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        sender_name = self.request.user.username

        # Retrieve the ManagerDecision object
        applicant = get_object_or_404(ManagerDecision, pk=self.kwargs['pk'])

        # Save the data to the EmailLog model
        EmailLog.objects.create(
            applicant=applicant.applicant,
            sender_name=sender_name,
            to_email=applicant.email,
            subject=subject,
            message=message
        )
        send_mail(
            subject,
            message,
            'EMAIL_HOST_USER',
            [applicant.email],
            fail_silently=False,
        )
        return super().form_valid(form)

class HRLogsView(UserPassesTestMixin, View):
    template_name = 'logs.html'

    def test_func(self):
        return self.request.user.is_authenticated 

    def get(self, request):
        job_applications = JobApplication.objects.all()
        meeting_schedules = MeetingSchedule.objects.all()
        teamLead_decisions = TeamLeadDecision.objects.all()
        manager_decisions = ManagerDecision.objects.all()
        send_mail = EmailLog.objects.all()
        return render(request, self.template_name, {'job_applications': job_applications, 'meeting_schedules': meeting_schedules, 'teamLead_decisions': teamLead_decisions, 'manager_decisions': manager_decisions, 'send_mail': send_mail})