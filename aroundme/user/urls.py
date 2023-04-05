from django.urls import path
from user.views import*

urlpatterns = [
    path('',UserHome.as_view(),name="uh"),
    path('profile',Profile.as_view(),name="pro"),
    path('addbio',BioView.as_view(),name="bio"),
    path('editbio/<int:pk>/',EditBio.as_view(),name="editbio"),
    path('editpass',EditPassword.as_view(),name="editpass"),
    path('mypost',MyPost.as_view(),name="mypost"),
    path('editpost/<int:pk>/',EditPost.as_view(),name="editpost"),
    path('delete/<int:pk>/',DeletePost.as_view(),name="delete"),
    path('addcmnt/<int:pid>/',addcomment,name="addcmnt"),
    path('addlike/<int:pid>/',addlike,name="addlike"),
]
