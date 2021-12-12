from django.urls import path
from rest_framework import routers
from .views import PollViewSet, ActivePolls, get_active_poll, CreateAnswer, get_my_poll

app_name = 'API_polling'
router = routers.DefaultRouter()
router.register('admin/polls', PollViewSet, basename='polls')

urlpatterns = [
    path('api/polls', ActivePolls.as_view(), name='active_polls'),
    path('api/polls/<int:pk>', get_active_poll, name='active_poll_detail'),
    path('api/polls/<int:pk>/answer', CreateAnswer.as_view(), name='answer_active_poll'),
    path('api/mypoll/<int:pk>', get_my_poll, name='my_poll')
]
urlpatterns += router.urls
