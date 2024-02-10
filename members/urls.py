from django.urls import path
from . import views

urlpatterns = [
    path('api/all',views.all_Member,),
    path('api/add',views.add_Member,),
    path('api/delete/<int:ID>',views.delete_Member,),
    path('api/update/<int:ID>',views.update_Member,),
]
