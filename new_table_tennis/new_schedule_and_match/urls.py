from django.urls import path

from .views import ListSchedule

urlpatterns = [
    path('schedules/', ListSchedule.as_view(), name='list-schedule'),
]

from .views import ViewSchedule

urlpatterns += [
    path('schedules/<int:id_schedule>/', ViewSchedule.as_view(), name='view-schedule'),
]

from .views import ListMatch

urlpatterns += [
    path('matches/', ListMatch.as_view(), name='list-match'),
]

from .views import ViewMatch

urlpatterns += [
    path('matches/<int:id_match>/', ViewMatch.as_view(), name='view-match'),
]

from .views import ListPendingFeedback

urlpatterns += [
    path('pending_feedbacks/', ListPendingFeedback.as_view(), name='list-pending-feedback'),
]

from .views import ViewPendingFeedback

urlpatterns += [
    path('pending_feedbacks/<int:id_pending_feedback>/', ViewPendingFeedback.as_view(), name='view-pending-feedback'),
]

from .views import ListCompletedFeedback

urlpatterns += [
    path('completed_feedbacks/', ListCompletedFeedback.as_view(), name='list-completed-feedback'),
]

from .views import ViewCompletedFeedback

urlpatterns += [
    path('completed_feedbacks/<int:id_completed_feedback>/', ViewCompletedFeedback.as_view(), name='view-completed-feedback'),
]

from .views import ListPendingResults

urlpatterns += [
    path('pending_results/', ListPendingResults.as_view(), name='list-pending-results'),
]

from .views import ViewPendingResult

urlpatterns += [
    path('pending_results/<int:id_pending_result>/', ViewPendingResult.as_view(), name='view-pending-result'),
]

from .views import ListCompletedResults

urlpatterns += [
    path('completed_results/', ListCompletedResults.as_view(), name='list-completed-results'),
]

from .views import ViewCompletedResult

urlpatterns += [
    path('completed_results/<int:id_completed_result>/', ViewCompletedResult.as_view(), name='view-completed-result'),
]

from .views import AcceptMatch

urlpatterns += [
    path('matches/<int:id_match>/accept', AcceptMatch.as_view(), name='accept-match'),
]

from .views import RejectMatch

urlpatterns += [
    path('matches/<int:id_match>/reject', RejectMatch.as_view(), name='reject-match'),
]

from .views import DeleteMatch

urlpatterns += [
    path('matches/<int:id_match>/delete', DeleteMatch.as_view(), name='delete-match'),
]
