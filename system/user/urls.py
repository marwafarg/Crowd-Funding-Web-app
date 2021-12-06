from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup.as_view(),name='signup'),
    path('profile/',profile,name='profile'),
    path('', login, name='login'),
    path('account/', account, name='account'),

    path('logout/', logout, name='logout'),
    path('setting/', AccountSttingView.as_view(), name='setting'),


]