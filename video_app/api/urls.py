from django.urls import path
from .views import VideoListView, VideoDetailView, UserVideoProgressListView, UserVideoProgressDetailView


urlpatterns = [
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(),
         name='video-detail'),
    path('progress/', UserVideoProgressListView.as_view(), name='progress-list'),
    path('progress/<int:pk>/', UserVideoProgressDetailView.as_view(),
         name='progress-detail'),

]
