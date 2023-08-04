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

from .views import SubmitFeedback

urlpatterns += [
    path('pending_feedbacks/<int:id_pending_feedback>/', SubmitFeedback.as_view(), name='submit-feedback'),
]

from .views import ListCompletedFeedback

urlpatterns += [
    path('completed_feedbacks/', ListCompletedFeedback.as_view(), name='list-completed-feedback'),
]
