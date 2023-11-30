from django.urls import include, path
from django import urls
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', home.as_view(), name='home'),
    path('all-jobs/', AllJobs.as_view(), name='all_jobs'),
    path('job/<int:pk>/', JobDetail.as_view(), name='job_detail'),
    path('apply-now/<int:job_id>/', ApplyNowView.as_view(), name='apply_now'),
    path('accounts/login/', CustomLoginView.as_view(), name='custom_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='custom_logout'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('release_job/', ReleaseJobView.as_view(), name='release_job'),
    path('view_job_applications/', ViewJobApplications.as_view(), name='view_job_applications'),
    path('view-applicants/<slug:job_slug>/', ViewApplicants.as_view(), name='view_applicants'),
    path('view-profile/<slug:applicant_slug>/', ViewProfile.as_view(), name='view_profile'),
    path('accept-by-hr/<slug:job_slug>/', ViewApplicants.as_view(), name='accept-by-hr'),


    path('view_scheduled_meetings/', ViewScheduledMeetings.as_view(), name='view_scheduled_meetings'),
    path('review_meeting/<int:meeting_id>/', ReviewMeetingView.as_view(), name='review_meeting'),
    path('all_candidate_reviews/', AllCandidateReviewsView.as_view(), name='all_candidate_reviews'),
    path('candidate_reviews/<int:applicant_id>/', CandidateReviewsView.as_view(), name='candidate_reviews'),
    path('give_decision/<int:applicant_id>/', TeamLeadDecisionView.as_view(), name='give_decision'),
    path('accepted_candidates_by_team_lead/', AcceptedCandidatesbyTeamLead.as_view(), name='accepted_candidates_by_team_lead'),
    path('manager_decision/<str:applicant>/', ManagerDecisionView.as_view(), name='manager_decision_view'),
    path('accepted_candidates_by_manager/', AcceptedCandidatesbyManager.as_view(), name='accepted_candidates_by_manager'),
    path('send_email/<int:pk>/', SendEmail.as_view(), name='send_email'),

    path('logs/', HRLogsView.as_view(), name='logs'),
    
    

]
