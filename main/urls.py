from django.urls import include, path
from django import urls
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', home.as_view(), name='home'),
    path('all-jobs/', AllJobs.as_view(), name='all_jobs'),
    path('applied-jobs/', AppliedJobs.as_view(), name='applied_jobs'),
    path('job/<int:pk>/', JobDetail.as_view(), name='job_detail'),
    path('apply-now/<int:job_id>/', ApplyNowView.as_view(), name='apply_now'),
    path('accounts/login/', CustomLoginView.as_view(), name='custom_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='custom_logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('release_job/', ReleaseJobView.as_view(), name='release_job'),
    path('view_job_applications/', ViewJobApplications.as_view(), name='view_job_applications'),
    path('view-applicants/<slug:job_slug>/', ViewApplicants.as_view(), name='view_applicants'),
    path('view-profile/<slug:applicant_slug>/', ViewProfile.as_view(), name='view_profile'),
    path('view_scheduled_meetings/', ViewScheduledMeetings.as_view(), name='view_scheduled_meetings'),
    path('review_meeting/<slug:applicant_slug>/', ReviewMeetingView.as_view(), name='review_meeting'),
    path('sent-by-mainHr/', SentByMainHr.as_view(), name='sent_by_mainHr'),



]
