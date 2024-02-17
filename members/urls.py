from django.urls import path
from . import views

urlpatterns = [
    path('member/api/all',views.all_Member,),
    path('member/api/add',views.add_Member,),
    path('member/api/delete/<int:ID>',views.delete_Member,),
    path('member/api/update/<int:ID>',views.update_Member,),
]
