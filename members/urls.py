from django.urls import path
from . import views

urlpatterns = [
    path("members/", views.Member_list),
    path("members/<int:pk>/", views.Member_detail),
]
