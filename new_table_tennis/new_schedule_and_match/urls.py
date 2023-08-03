from django.urls import path
from .views import ListSchedule

urlpatterns = [
    path('schedules/', ListSchedule.as_view(), name='list-schedule'),
]

from .views import SubmitSchedule

urlpatterns += [
    path('schedules/', SubmitSchedule.as_view(), name='submit-schedule'),
]

from .views import ViewSchedule

urlpatterns += [
    path('schedules/<int:id_schedule>/', ViewSchedule.as_view(), name='view-schedule'),
]

from .views import DeleteSchedule

urlpatterns += [
    path('schedules/<int:id_schedule>/', DeleteSchedule.as_view(), name='delete-schedule'),
]
