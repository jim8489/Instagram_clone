from django.urls import path
from userauth.views import *

urlpatterns = [
    path('<username>/', UserProfile, name="user_profile"),
    path('<username>/saved/', UserProfile, name="saved_posts"),
    path('<username>/follow/<option>', follow, name="follow"),
    path('profile/edit', profile_edit, name="profile_edit"),
    path('profile/create', ProfileCreateView.as_view(), name="profile_create"),


]