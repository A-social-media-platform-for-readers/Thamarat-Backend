from django.urls import path
from . import views


urlpatterns = [
    path('/member',views.read_all_Members,),
    path('/member/<int:ID>',views.read_one_Member,),
    path('/member',views.create_Member,),
    path('/member/<int:ID>',views.delete_Member,),
    path('/member/<int:ID>',views.update_Member,),
    path('/member/<int:ID>',views.update_whole_Member,),
]
