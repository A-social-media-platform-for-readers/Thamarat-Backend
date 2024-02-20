from django.urls import path
from . import views

urlpatterns = [
    path('member/api/all',views.all_Member,),
    path('member/api/add',views.add_Member,),
    path('member/api/delete/<int:ID>',views.delete_Member,),
    path('member/api/update/<int:ID>',views.update_Member,),
]


"""
urlpatterns = [
    path('/member',views.read_all_Members,),
    path('/member/<int:ID>',views.read_one_Member,),
    path('/member',views.create_Member,),
    path('/member/<int:ID>',views.delete_Member,),
    path('/member/<int:ID>',views.update_Member,),
    path('/member/<int:ID>',views.update_whole_Member,),
]
"""